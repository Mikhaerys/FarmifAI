// Archivo: ChatbotOrchestrator.kt
package edu.unicauca.app.agrochat // O el paquete que corresponda

// No se necesita Context aquí si MindSporeHelper ya está inicializado
import android.util.Log
import edu.unicauca.app.agrochat.mindspore.MindSporeHelper
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class ChatbotOrchestrator(
    private val mindSporeHelper: MindSporeHelper, // RECIBE LA INSTANCIA
    private val coroutineScope: CoroutineScope    // Para lanzar operaciones asíncronas de predicción
) {
    // Ya no necesitamos crear una instancia de mindSporeHelper aquí
    // private var isChatbotReady = false // Se asume que el helper ya está listo o se verificará

    // Nombres de los tensores (¡DEBES CAMBIARLOS POR LOS REALES DE TU MODELO!)
    private val inputTensorName = "0"
    private val outputTensorName = "0"

    companion object {
        private const val TAG = "ChatbotOrchestrator"
    }

    // El bloque init ya no necesita inicializar MindSporeHelper
    // init {
    //     // La inicialización ahora ocurre fuera, en MainActivity
    // }

    /**
     * Simula la obtención de una predicción.
     * En una app real, los tokenIds vendrían de tu tokenizador.
     */
    suspend fun getDummyPrediction() {
        // Verificar si el helper que nos pasaron está realmente inicializado
        if (!mindSporeHelper.isInitialized) {
            Log.e(TAG, "MindSporeHelper no está inicializado. No se puede realizar la predicción.")
            return
        }

        // --- Simulación de Entrada ---
        // (Igual que antes, asegúrate de que el tamaño es correcto para tu modelo)
        val dummyTokenIdsAsFloat = IntArray(64) { i -> i % 30522 }
        Log.d(TAG, "Datos de entrada (primeros 10): ${dummyTokenIdsAsFloat.take(10).joinToString()}")

        // --- Llamada a la Inferencia ---
        Log.d(TAG, "Llamando a mindSporeHelper.predictRaw...")
        val outputLogits: FloatArray? = withContext(Dispatchers.Default) {
            mindSporeHelper.predictRaw(
                inputTensorName = inputTensorName,
                outputTensorName = outputTensorName,
                inputArray = dummyTokenIdsAsFloat
            )
        }

        // --- Procesamiento de la Salida ---
        if (outputLogits != null) {
            Log.i(TAG, "Predicción cruda recibida exitosamente.")
            Log.d(TAG, "Número de logits de salida: ${outputLogits.size}")

            val outputPreview = outputLogits.take(20).joinToString(", ") {
                String.format(Locale.US, "%.4f", it)
            }
            Log.d(TAG, "Primeros ${outputLogits.take(20).size} logits de salida: [$outputPreview]")

            val nextTokenId = findNextTokenId(outputLogits)
            Log.i(TAG, "Siguiente ID de token (ejemplo con argmax): $nextTokenId (valor: ${outputLogits[nextTokenId]})")

        } else {
            Log.e(TAG, "La predicción cruda falló o devolvió null.")
        }
    }

    private fun findNextTokenId(logits: FloatArray): Int {
        if (logits.isEmpty()) return -1
        var maxIdx = 0
        var maxValue = logits[0]
        for (i in 1 until logits.size) {
            if (logits[i] > maxValue) {
                maxValue = logits[i]
                maxIdx = i
            }
        }
        return maxIdx
    }

    // El método cleanup aquí ya no necesita llamar a mindSporeHelper.release()
    // porque MainActivity es el propietario de mindSporeHelper y lo liberará en su onDestroy.
    // fun cleanup() {
    //     Log.d(TAG, "ChatbotOrchestrator limpiado (MindSporeHelper es manejado externamente).")
    // }
}
