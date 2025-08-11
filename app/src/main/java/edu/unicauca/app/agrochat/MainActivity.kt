package edu.unicauca.app.agrochat

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column // Para añadir un botón de prueba
import androidx.compose.foundation.layout.Spacer // Para espaciado
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height // Para espaciado
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button // Para el botón de prueba
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue // Eliminado 'remember' si no se usa directamente aquí
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp // Para el espaciado
import androidx.lifecycle.lifecycleScope
import edu.unicauca.app.agrochat.mindspore.MindSporeHelper
import edu.unicauca.app.agrochat.ui.theme.AgroChatTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {

    private lateinit var mindSporeHelper: MindSporeHelper
    private var mindSporeStatus by mutableStateOf("Inicializando MindSpore...")

    // NUEVO: Instancia del ChatbotOrchestrator
    private var chatbotOrchestrator: ChatbotOrchestrator? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        mindSporeHelper = MindSporeHelper(applicationContext)

        lifecycleScope.launch {
            val success = mindSporeHelper.initialize()
            if (success) {
                mindSporeStatus = "MindSpore Helper inicializado exitosamente."
                Log.i("MainActivity", mindSporeStatus)

                // NUEVO: Crear ChatbotOrchestrator una vez que MindSporeHelper está listo
                chatbotOrchestrator = ChatbotOrchestrator(mindSporeHelper, lifecycleScope)
                Log.i("MainActivity", "ChatbotOrchestrator creado.")

                // Opcional: Ejecutar una prueba de predicción inmediatamente después de la inicialización
                // chatbotOrchestrator?.getDummyPrediction() // Descomenta para probar

            } else {
                mindSporeStatus = "Fallo al inicializar MindSpore Helper."
                Log.e("MainActivity", mindSporeStatus)
            }
        }

        setContent {
            AgroChatTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    // Modificamos MainScreen para incluir un botón de prueba
                    MainScreenWithTestButton(
                        statusMessage = mindSporeStatus,
                        isChatbotReady = chatbotOrchestrator != null && mindSporeHelper.isInitialized,
                        onTestPredictionClicked = {
                            lifecycleScope.launch { // Asegúrate de que las llamadas a suspend fun sean desde una corrutina
                                chatbotOrchestrator?.getDummyPrediction()
                            }
                        },
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        // `ChatbotOrchestrator` ya no gestiona `mindSporeHelper.release()`
        // `mindSporeHelper` se libera aquí como propietario
        if (::mindSporeHelper.isInitialized) { // Buena práctica verificar antes de llamar
            mindSporeHelper.release()
        }
        Log.d("MainActivity", "MindSporeHelper liberado en onDestroy de MainActivity.")
    }
}

// Modificamos MainScreen para añadir un botón y probar la predicción
@Composable
fun MainScreenWithTestButton(
    statusMessage: String,
    isChatbotReady: Boolean,
    onTestPredictionClicked: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = statusMessage)
            Spacer(modifier = Modifier.height(16.dp))
            if (isChatbotReady) {
                Button(onClick = onTestPredictionClicked) {
                    Text("Probar Predicción")
                }
            } else {
                Text("Chatbot no está listo aún...")
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun MainScreenWithTestButtonPreview() {
    AgroChatTheme {
        MainScreenWithTestButton(
            "MindSpore Helper inicializado exitosamente.",
            isChatbotReady = true,
            onTestPredictionClicked = {}
        )
    }
}

// ... (Greeting y GreetingPreview pueden permanecer o eliminarse si no se usan)
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    AgroChatTheme {
        Greeting("Android")
    }
}
