package edu.unicauca.app.agrochat.mindspore

import android.content.Context
import android.content.res.AssetManager
import android.util.Log
import com.mindspore.Model
import com.mindspore.MSTensor
import com.mindspore.config.CpuBindMode
import com.mindspore.config.DataType
import com.mindspore.config.DeviceType
import com.mindspore.config.MSContext
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.io.InputStream
import java.io.RandomAccessFile
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.FloatBuffer
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MindSporeHelper(private val androidContext: Context) {

    companion object {
        private const val TAG = "MindSporeHelper"

        init {
            try {
                System.loadLibrary("mindspore-lite-jni")
                Log.i(TAG, "Librerías nativas MindSpore cargadas explícitamente.")
            } catch (e: UnsatisfiedLinkError) {
                Log.e(TAG, "Error al cargar librerías nativas MindSpore explícitamente.", e)
            }
        }
    }

    private var msModel: Model? = null
    private var msContext: MSContext? = null
    private val modelNameInAssets =
        "gpt2_fp16_model.ms" // Asegúrate de que este es el nombre correcto
    private var modelFileOnDevice: File? = null

    // Para la prueba de mantener los descriptores de archivo abiertos
    private var openedFileChannel: FileChannel? = null
    private var openedRandomAccessFile: RandomAccessFile? = null

    val isInitialized: Boolean
        get() = msModel != null && msContext != null

    @Throws(IOException::class)
    private fun copyAssetToCache(assetFileName: String): File {
        val assetManager: AssetManager = androidContext.assets
        var inputStream: InputStream? = null
        var outputStream: FileOutputStream? = null
        val outputFile: File
        try {
            Log.d(TAG, "Intentando abrir '$assetFileName' desde assets.")
            inputStream = assetManager.open(assetFileName)
            Log.d(
                TAG,
                "InputStream para '$assetFileName' disponible, bytes aproximados: ${inputStream.available()}"
            )

            val cacheDir = androidContext.cacheDir
            outputFile = File(cacheDir, assetFileName)
            Log.d(TAG, "Ruta del archivo en caché: ${outputFile.absolutePath}")

            if (outputFile.exists()) {
                Log.d(
                    TAG,
                    "Archivo '$assetFileName' ya existe en caché. Tamaño: ${outputFile.length()} bytes."
                )
                if (outputFile.length() > 0) {
                    // Si ya existe y tiene contenido, no necesitamos verificar el tamaño del asset
                    // a menos que queramos implementar una lógica de sobreescritura si el asset es más nuevo.
                    Log.d(TAG, "Usando archivo existente de caché: ${outputFile.absolutePath}")
                    return outputFile
                } else {
                    Log.w(
                        TAG,
                        "Archivo '$assetFileName' existe en caché PERO está VACÍO. Se intentará sobreescribir."
                    )
                }
            }

            Log.d(TAG, "Procediendo a copiar '$assetFileName' a la caché.")
            outputStream = FileOutputStream(outputFile) // Crea o trunca el archivo
            val buffer = ByteArray(4 * 1024)
            var read: Int
            var totalBytesCopied = 0L
            while (inputStream.read(buffer).also { read = it } != -1) {
                outputStream.write(buffer, 0, read)
                totalBytesCopied += read
            }
            outputStream.flush()
            Log.d(
                TAG,
                "Copia finalizada. Total de bytes copiados para '$assetFileName': $totalBytesCopied"
            )
            Log.d(
                TAG,
                "Tamaño final del archivo en caché '${outputFile.name}': ${outputFile.length()} bytes."
            )

            if (totalBytesCopied == 0L && inputStream.available() > 0) { // inputStream.available() podría ser 0 después de leerlo
                Log.w(
                    TAG,
                    "Advertencia: Se copiaron 0 bytes pero el asset podría no estar vacío inicialmente. Verifica el asset original."
                )
            }
            if (outputFile.length() == 0L && totalBytesCopied > 0L) {
                Log.e(
                    TAG,
                    "ERROR CRÍTICO: Se copiaron $totalBytesCopied bytes, ¡pero el archivo en caché sigue teniendo tamaño 0!"
                )
            }

            return outputFile
        } catch (e: IOException) {
            Log.e(TAG, "IOException durante copyAssetToCache para '$assetFileName'", e)
            throw e // Relanzar para que sea manejado por el llamador
        } finally {
            try {
                inputStream?.close()
            } catch (e: IOException) {
                Log.w(TAG, "IOException al cerrar inputStream para '$assetFileName'", e)
            }
            try {
                outputStream?.close()
            } catch (e: IOException) {
                Log.w(TAG, "IOException al cerrar outputStream para '$assetFileName'", e)
            }
        }
    }


    /**
     * Carga el archivo del modelo en un MappedByteBuffer.
     * MODIFICADO PARA PRUEBA: No cierra FileChannel/RandomAccessFile aquí.
     * Se cerrarán en el método release().
     */
    private fun loadModelFileToByteBuffer(modelFile: File): MappedByteBuffer? {
        // Cerrar los anteriores si existen (limpieza de prueba anterior)
        closeFileDescriptors()

        return try {
            openedRandomAccessFile = RandomAccessFile(modelFile, "r")
            openedFileChannel = openedRandomAccessFile!!.channel
            val mappedByteBuffer = openedFileChannel!!.map(
                FileChannel.MapMode.READ_ONLY,
                0,
                openedFileChannel!!.size()
            )
            mappedByteBuffer?.load() // Opcional, pero puede ayudar a asegurar que esté en memoria.
            Log.d(
                TAG,
                "Modelo '${modelFile.name}' cargado en MappedByteBuffer desde: ${modelFile.absolutePath}, size: ${openedFileChannel!!.size()}"
            )
            mappedByteBuffer
        } catch (e: IOException) {
            Log.e(TAG, "IOException al cargar modelo '${modelFile.name}' en MappedByteBuffer", e)
            closeFileDescriptors() // Asegurar cierre en caso de error
            null
        }
        // No hay bloque finally para cerrar aquí durante la prueba
    }

    private fun createAndConfigureMSContextForCPU(): MSContext? {
        val tempContext = MSContext()
        try {
            tempContext.init(2, CpuBindMode.NO_BIND) // 2 hilos, sin afinidad específica
            Log.d(TAG, "MSContext: Número de hilos configurado (2), modo de afinidad a NO_BIND.")

            val addDeviceSuccess =
                tempContext.addDeviceInfo(DeviceType.DT_CPU, true) // Habilitar FP16 si es soportado
            if (!addDeviceSuccess) {
                Log.e(TAG, "Fallo al añadir dispositivo CPU al MSContext.")
                tempContext.free()
                return null
            }
            Log.d(
                TAG,
                "MSContext creado y configurado para CPU (Float16 habilitado si es soportado)."
            )
            return tempContext
        } catch (e: Exception) {
            Log.e(TAG, "Excepción al inicializar o configurar MSContext: ${e.message}", e)
            tempContext.free()
            return null
        }
    }

    suspend fun initialize(): Boolean {
        if (isInitialized) {
            Log.i(TAG, "MindSporeHelper ya inicializado.")
            return true
        }

        // Liberar recursos previos
        releaseInternalResources() // Solo libera MindSpore, no los descriptores de archivo aún

        return withContext(Dispatchers.IO) {
            val copiedModelFile = try {
                copyAssetToCache(modelNameInAssets)
            } catch (e: IOException) {
                Log.e(TAG, "Fallo al copiar el modelo desde assets.", e)
                return@withContext false
            }
            modelFileOnDevice = copiedModelFile

            val modelByteBuffer = loadModelFileToByteBuffer(copiedModelFile)
            if (modelByteBuffer == null) {
                Log.e(TAG, "Fallo al cargar el modelo en MappedByteBuffer.")
                // Los descriptores de archivo ya se habrían cerrado en loadModelFileToByteBuffer si hubo error allí
                return@withContext false
            }

            // Log detallado del MappedByteBuffer
            Log.d(
                TAG,
                "Antes de model.build: modelByteBuffer capacity=${modelByteBuffer.capacity()}, " +
                        "isDirect=${modelByteBuffer.isDirect}, position=${modelByteBuffer.position()}, " +
                        "limit=${modelByteBuffer.limit()}"
            )

            val tempContext = createAndConfigureMSContextForCPU()
            if (tempContext == null) {
                Log.e(TAG, "Fallo al crear MSContext.")
                closeFileDescriptors() // Si el contexto falla, cerramos los descriptores
                return@withContext false
            }

            val model = Model()
            val modelTypeInt = 4 // Asumiendo ModelType.MINDIR_LITE

            Log.d(TAG, "Intentando construir el modelo con modelType (Int): $modelTypeInt")
            val buildSuccess = try {
                model.build(modelByteBuffer, modelTypeInt, tempContext)
            } catch (e: Exception) {
                Log.e(TAG, "Excepción durante model.build: ${e.message}", e)
                false
            }

            if (buildSuccess) {
                msModel = model
                msContext = tempContext
                Log.i(TAG, "Modelo construido (compilado) exitosamente. MindSporeHelper listo.")
                true
            } else {
                Log.e(TAG, "Fallo al construir (compilar) el modelo.")
                tempContext.free() // Liberar el contexto si la compilación del modelo falla
                closeFileDescriptors() // Importante cerrar los descriptores si build falla
                false
            }
        }
    }

    private fun releaseInternalResources() {
        msModel?.free()
        msModel = null
        msContext?.free()
        msContext = null
    }

    private fun closeFileDescriptors() {
        try {
            openedFileChannel?.close()
        } catch (e: IOException) {
            Log.w(TAG, "IOException al cerrar FileChannel.", e)
        }
        try {
            openedRandomAccessFile?.close()
        } catch (e: IOException) {
            Log.w(TAG, "IOException al cerrar RandomAccessFile.", e)
        }
        openedFileChannel = null
        openedRandomAccessFile = null
    }

    fun release() {
        Log.d(TAG, "Liberando recursos de MindSporeHelper.")
        releaseInternalResources()
        closeFileDescriptors() // Asegurar que los descriptores de archivo se cierren aquí
        Log.d(TAG, "Recursos de MindSporeHelper liberados.")
    }

    private fun floatArrayToByteBuffer(data: FloatArray): ByteBuffer {
        val byteBuffer = ByteBuffer.allocateDirect(data.size * 4)
        byteBuffer.order(ByteOrder.LITTLE_ENDIAN)
        val floatBuffer: FloatBuffer = byteBuffer.asFloatBuffer()
        floatBuffer.put(data)
        byteBuffer.rewind()
        return byteBuffer
    }

    fun predictRaw(
        inputTensorName: String,
        outputTensorName: String,
        inputArray: IntArray   // debe ser IntArray porque es int32
    ): FloatArray? {

        if (!isInitialized || msModel == null) {
            Log.e(TAG, "El modelo no está inicializado o es nulo.")
            return null
        }

        try {
            Log.d(TAG, "Creando tensor de entrada automáticamente desde IntArray...")

            // ✅ CREA EL TENSOR DIRECTAMENTE CON LA API SIMPLE
            val inputTensor = MSTensor.createTensor(inputTensorName, inputArray)

            val inputs = mutableListOf(inputTensor)
            val outputs = mutableListOf<MSTensor>()

            Log.d(TAG, "Ejecutando model.predict(inputs, outputs)...")
            val success = msModel!!.predict()
            if (!success) {
                Log.e(TAG, "predict() falló")
                return null
            }

            // Buscar el tensor de salida por nombre
            val outputTensor = outputs.find { it.tensorName() == outputTensorName }
            if (outputTensor == null) {
                Log.e(TAG, "No se encontró el tensor de salida: $outputTensorName")
                return null
            }

            val results = outputTensor.floatData
            if (results == null) {
                Log.e(TAG, "outputTensor.floatData es null para '$outputTensorName'")
                return null
            }

            return results

        } catch (e: Exception) {
            Log.e(TAG, "Excepción en predictRaw: ${e.message}", e)
            return null
        }
    }

}





