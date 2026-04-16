package edu.unicauca.app.agrochat.models

import android.content.Context
import java.io.File

/**
 * Registro local de artefactos de IA provisionados en `files/models`.
 *
 * No realiza llamadas de red ni modifica el conjunto de modelos disponible.
 */
class LocalModelRegistry private constructor() {

    companion object {
        private const val MIN_MODEL_BYTES = 1024L

        @Volatile
        private var instance: LocalModelRegistry? = null

        fun getInstance(): LocalModelRegistry {
            return instance ?: synchronized(this) {
                instance ?: LocalModelRegistry().also { instance = it }
            }
        }
    }

    fun getModelsDir(context: Context): File {
        val dir = File(context.filesDir, "models")
        if (!dir.exists()) dir.mkdirs()
        return dir
    }

    fun isModelAvailable(context: Context, modelName: String): Boolean {
        val modelFile = File(getModelsDir(context), modelName)
        return modelFile.exists() && modelFile.length() > MIN_MODEL_BYTES
    }

    fun getModelPath(context: Context, modelName: String): String? {
        val modelFile = File(getModelsDir(context), modelName)
        return if (isModelAvailable(context, modelName)) modelFile.absolutePath else null
    }
}
