package edu.unicauca.app.agrochat.feedback

import android.content.Context
import edu.unicauca.app.agrochat.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone
import java.util.UUID

/**
 * Almacena eventos de retroalimentacion en JSONL local para analisis de campo.
 *
 * Ruta:
 * files/feedback/feedback_events_YYYY-MM-DD.jsonl
 */
class FeedbackEventStore(context: Context) {
    private val appContext = context.applicationContext
    private val rootDir = File(appContext.filesDir, "feedback").apply { mkdirs() }
    private val fileLock = Any()
    private val dayFormatter = SimpleDateFormat("yyyy-MM-dd", Locale.US)
    private val localFormatter = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.US)
    private val isoFormatter = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSZ", Locale.US)
    private val manifestFile = File(rootDir, "feedback_manifest.json")

    fun storagePath(): String = rootDir.absolutePath
    fun syncManifestPath(): String = manifestFile.absolutePath
    fun pendingLivePath(): String = ""

    suspend fun recordAssistantResponse(
        sessionId: String,
        messageId: String,
        turnIndex: Int,
        userQuery: String,
        assistantResponse: String,
        responseLabel: String,
        usedLlm: Boolean,
        kbSupported: Boolean,
        kbSupportScore: Float,
        kbCoverage: Float,
        kbUnknownRatio: Float
    ) {
        val now = System.currentTimeMillis()
        val event = baseEvent("assistant_response", now, sessionId, messageId)
            .put("turn_index", turnIndex)
            .put("response_label", responseLabel)
            .put("used_llm", usedLlm)
            .put("kb_supported", kbSupported)
            .put("kb_support_score", kbSupportScore.toDouble())
            .put("kb_coverage", kbCoverage.toDouble())
            .put("kb_unknown_ratio", kbUnknownRatio.toDouble())
            .put("user_query", userQuery.take(1200))
            .put("assistant_response", assistantResponse.take(2400))

        appendEvent(now, event)
    }

    suspend fun recordFeedbackUpdate(
        sessionId: String,
        messageId: String,
        responseLabel: String,
        userQuery: String,
        assistantResponse: String,
        helpful: Boolean?,
        clear: Boolean?,
        wouldApplyToday: Boolean?
    ) {
        val now = System.currentTimeMillis()
        val event = baseEvent("feedback_update", now, sessionId, messageId)
            .put("response_label", responseLabel)
            .put("helpful", helpful)
            .put("clear", clear)
            .put("would_apply_today", wouldApplyToday)
            .put("user_query", userQuery.take(1200))
            .put("assistant_response", assistantResponse.take(2400))

        appendEvent(now, event)
    }

    private fun baseEvent(
        type: String,
        nowMs: Long,
        sessionId: String,
        messageId: String
    ): JSONObject {
        return JSONObject()
            .put("event_id", UUID.randomUUID().toString())
            .put("event_type", type)
            .put("timestamp_ms", nowMs)
            .put("timestamp_local", localFormatter.format(Date(nowMs)))
            .put("timestamp_iso", isoFormatter.format(Date(nowMs)))
            .put("timezone_id", TimeZone.getDefault().id)
            .put("session_id", sessionId)
            .put("message_id", messageId)
            .put("app_version", BuildConfig.VERSION_NAME)
            .put("app_package", BuildConfig.APPLICATION_ID)
    }

    private suspend fun appendEvent(nowMs: Long, event: JSONObject) = withContext(Dispatchers.IO) {
        val outFile = File(rootDir, "feedback_events_${dayFormatter.format(Date(nowMs))}.jsonl")
        synchronized(fileLock) {
            outFile.parentFile?.mkdirs()
            outFile.appendText(event.toString() + "\n")
            writeManifestLocked(outFile, nowMs)
        }
    }

    private fun writeManifestLocked(outFile: File, nowMs: Long) {
        val manifest = JSONObject()
            .put("format", "feedback_local_manifest_v1")
            .put("updated_at_ms", nowMs)
            .put("updated_at_local", localFormatter.format(Date(nowMs)))
            .put("updated_at_iso", isoFormatter.format(Date(nowMs)))
            .put("timezone_id", TimeZone.getDefault().id)
            .put("latest_file", outFile.name)
            .put("latest_file_size_bytes", outFile.length())
            .put("latest_file_line_count", outFile.useLines { lines -> lines.count() })

        manifestFile.parentFile?.mkdirs()
        manifestFile.writeText(manifest.toString(2))
    }
}
