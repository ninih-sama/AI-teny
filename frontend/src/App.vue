<template>
  <div class="font-sans antialiased bg-[#EDF2F9] min-h-screen text-slate-900">
    
    <transition name="fade">
      <div v-if="isLoading" class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-[#EDF2F7]">
        <div class="mb-8">
          <div class="text-8xl font-black tracking-tighter text-slate-950 animate-pulse-slow">
            AI<span class="text-red-600">-teny</span>
          </div>
        </div>
        
        <div class="w-40 h-[2px] bg-slate-300 rounded-full overflow-hidden relative">
          <div class="absolute inset-0 bg-red-600 animate-progress-fast"></div>
        </div>
        
        <p class="mt-6 text-[9px] font-black tracking-[0.5em] text-slate-400 uppercase">
          Fampidirana...
        </p>
      </div>
    </transition>

    <div v-if="!isLoading" class="page-enter">
      <Editor />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Editor from './components/Editor.vue'

const isLoading = ref(true)
const isSpeaking = ref(false) // Pour gérer l'animation du bouton


onMounted(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
  // Charger les voix pour le TTS (Correctif pour Chrome/Brave)
  window.speechSynthesis.getVoices()
  if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = window.speechSynthesis.getVoices
  }
})

const speakText = () => {
  let text = quill.getText().trim();
  if (!text) return;

  // --- MOTEUR DE PHONÉTIQUE MALAGASY ---
  // On transforme le texte pour que le moteur FR le lise avec l'accent local
  let phoneticText = text
    .replace(/o/g, 'ou')      // En MG, 'o' se prononce 'ou' (ex: 'mora' -> 'moura')
    .replace(/O/g, 'Ou')
    .replace(/j/g, 'dz')      // 'j' se prononce 'dz' (ex: 'joa' -> 'dzoa')
    .replace(/y(\s|$|[.,!])/g, 'i$1') // 'y' final se prononce 'i' (ex: 'mamy' -> 'mami')
    .replace(/ao/g, 'ow')     // 'ao' se prononce 'ow' (ex: 'tarao' -> 'tarow')
    .replace(/tr/g, 't-r')    // Force l'explosion du 'tr'
    .replace(/dr/g, 'd-r');   // Force l'explosion du 'dr'

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(phoneticText);
  
  // On récupère les voix
  const voices = window.speechSynthesis.getVoices();
  
  // Priorité : Italien (le top pour le MG) > Français > Défaut
  const bestVoice = voices.find(v => v.lang.includes('it-IT')) || 
                    voices.find(v => v.lang.includes('fr-FR')) || 
                    voices[0];
  
  utterance.voice = bestVoice;
  utterance.rate = 0.75;  // Indispensable : le rythme malgache est calme
  utterance.pitch = 0.9;  // Un ton plus grave pour plus de naturel

  utterance.onstart = () => { isSpeaking.value = true; };
  utterance.onend = () => { isSpeaking.value = false; };
  
  window.speechSynthesis.speak(utterance);
};
</script>

<style>
/* ANIMATIONS NATIVES */
@keyframes progress {
  0% { left: -100%; width: 100%; }
  100% { left: 100%; width: 100%; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseSlow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.animate-progress-fast { animation: progress 1.2s infinite linear; }
.animate-pulse-slow { animation: pulseSlow 2s infinite ease-in-out; }
.page-enter { animation: fadeIn 0.8s ease-out forwards; }

.fade-leave-active { transition: opacity 0.5s ease; }
.fade-leave-to { opacity: 0; }
</style>