<template>
  <div class="min-h-screen p-4 md:p-12 bg-[#EDF2F9] relative">
    <div class="max-w-6xl mx-auto">
      
      <div class="mb-10 bg-white border border-slate-300/50 p-10 rounded-xl shadow-sm flex flex-col md:flex-row justify-between items-center gap-6">
        <div>
          <h1 class="text-6xl font-black tracking-tighter text-slate-950">
            AI<span class="text-red-600">-teny</span>
          </h1>
          <p class="text-slate-400 font-bold text-[10px] uppercase tracking-[0.5em] mt-2">Editeur texte Malagasy</p>
        </div>
        <div class="flex flex-col items-end gap-3">
          <div class="px-4 py-1.5 bg-emerald-100 text-emerald-700 rounded text-[9px] font-black uppercase tracking-widest border border-emerald-200">En ligne</div>
          <div class="text-[9px] text-red-600 font-black px-4 py-1 border border-red-200 bg-red-50 uppercase tracking-tighter tracking-widest">M2 - Machine Learning</div>
        </div>
      </div>

      <main class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div class="lg:col-span-8">
          <div class="bg-white border border-slate-300/60 rounded-xl overflow-hidden shadow-sm focus-within:border-red-500 transition-all">
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50">
              <div class="flex gap-1.5">
                <div class="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-slate-200"></div>
                <div class="w-2.5 h-2.5 rounded-full bg-emerald-400"></div>
              </div>
              <span class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Editeur Professionnel</span>
            </div>
            <div id="editor" class="h-[450px] text-slate-800"></div>
          </div>

          <div class="mt-6 flex flex-wrap items-center justify-between gap-4 px-1">
            <div class="flex gap-6 items-center">
              <div class="text-center">
                <p class="text-[9px] font-black text-slate-400 uppercase">Mots</p>
                <p class="text-xl font-black text-slate-900 leading-none">{{ wordCount }}</p>
              </div>
            </div>
            
            <div class="flex flex-wrap gap-2 items-center">
              <button @click="clear" class="text-slate-400 hover:text-red-600 font-bold text-[11px] uppercase tracking-widest transition-colors mr-4">Effacer</button>
              
              <button @click="triggerImport" class="flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg font-black text-[9px] uppercase tracking-widest transition-all shadow-sm">
                <svg class="w-3.5 h-3.5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                Importer
              </button>
              <input type="file" ref="fileInput" @change="handleImport" accept=".pdf" class="hidden" />

              <button @click="exportPDF" class="flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg font-black text-[9px] uppercase tracking-widest transition-all shadow-sm">
                <svg class="w-3.5 h-3.5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Exporter
              </button>

              <button @click="speakText" :disabled="isSpeaking" class="flex items-center gap-2 px-4 py-2.5 bg-white border border-slate-300 text-slate-700 hover:bg-emerald-50 rounded-lg font-black text-[9px] uppercase tracking-widest transition-all shadow-sm disabled:opacity-50">
                <svg v-if="!isSpeaking" class="w-3.5 h-3.5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path>
                </svg>
                <span v-else class="w-2.5 h-2.5 bg-emerald-600 rounded-full animate-ping"></span>
                {{ isSpeaking ? 'Famakiana...' : 'Ecouter' }}
              </button>

              <button @click="check" :disabled="isAnalyzing" class="px-8 py-3 bg-slate-900 text-white font-black hover:bg-red-600 transition-all disabled:opacity-50 ml-2 shadow-lg shadow-slate-200">
                <span v-if="!isAnalyzing" class="uppercase text-xs tracking-widest">Analyser</span>
                <span v-else class="uppercase text-xs tracking-widest animate-pulse">Analyse...</span>
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-4">
          <div class="bg-white p-6 rounded-xl border border-slate-300/60 shadow-sm sticky top-4 max-h-[80vh] overflow-y-auto">
            <h3 class="text-[9px] uppercase tracking-widest font-black text-emerald-600 mb-6 flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-emerald-600 rounded-full animate-pulse"></span>
              Suggestions
            </h3>

            <div v-if="correctionsOnly.length === 0" class="py-20 text-center border border-dashed border-slate-100 bg-slate-50/50 rounded-lg">
              <p class="text-slate-300 text-[9px] font-bold uppercase tracking-tighter">Aucune faute détectée</p>
            </div>

            <div v-else class="space-y-4">
              <div v-for="(item, index) in correctionsOnly" :key="index" 
                   class="group p-4 bg-white border border-slate-200 rounded-lg hover:border-red-400 hover:shadow-md transition-all cursor-pointer"
                   @click="applySingleCorrection(item, index)">
                <div class="flex justify-between items-start mb-2">
                  <span class="text-[9px] font-black text-red-500 uppercase tracking-widest">Faute</span>
                  <span class="text-[9px] text-slate-300 group-hover:text-red-400 font-bold uppercase">Corriger</span>
                </div>
                <p class="text-sm font-medium text-slate-400 line-through mb-1">{{ item.original }}</p>
                <p class="text-lg font-black text-slate-900">→ {{ item.suggestion }}</p>
                <p v-if="item.definition" class="mt-2 text-[10px] text-slate-500 italic bg-slate-50 p-2 rounded border border-slate-100 leading-relaxed">{{ item.definition }}</p>
              </div>

              <button @click="applyAll" class="w-full py-4 bg-emerald-600 text-white text-[10px] font-black uppercase tracking-widest hover:bg-emerald-700 transition-all shadow-lg shadow-emerald-100">
                Tout corriger
              </button>
            </div>
          </div>
        </div>
      </main>

      <div v-if="showContextMenu" 
           :style="{ top: menuY + 'px', left: menuX + 'px' }"
           class="fixed z-[9999] bg-white border border-slate-200 shadow-2xl rounded-xl overflow-hidden min-w-[240px] animate-in fade-in zoom-in duration-200">
        <div class="px-4 py-3 bg-slate-900 text-white flex justify-between items-center">
          <div>
            <p class="text-[8px] font-black uppercase tracking-[0.2em] opacity-50 mb-0.5">Traduction</p>
            <p class="text-sm font-bold">{{ selectedWord }}</p>
          </div>
          <button @click="showContextMenu = false" class="text-slate-400 hover:text-white">✕</button>
        </div>
        <div class="p-4 bg-white">
          <p class="text-xs text-slate-600 leading-relaxed italic">
            {{ lookupResult || 'Fikarohana...' }}
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Quill from 'quill'
import axios from 'axios'
import html2pdf from 'html2pdf.js'
import * as pdfjsLib from 'pdfjs-dist/build/pdf'
import 'quill/dist/quill.snow.css'

// Initialisation Worker PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`

// REFS
const correctionsOnly = ref([])
const fullCorrectedText = ref("")
const wordCount = ref(0)
const isAnalyzing = ref(false)
const isSpeaking = ref(false)
const fileInput = ref(null)

// REFS CLIC DROIT
const showContextMenu = ref(false)
const menuX = ref(0)
const menuY = ref(0)
const selectedWord = ref("")
const lookupResult = ref("")

let quill

onMounted(() => {
  quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: 'Soraty na ampidiro eto ny lahatsoratrao...',
    modules: { 
      toolbar: [
        ['bold', 'italic', 'underline'], 
        [{ 'header': 1 }, { 'header': 2 }],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['clean']
      ] 
    }
  })

  // Compteur de mots
  quill.on('text-change', () => {
    const text = quill.getText().trim()
    wordCount.value = text ? text.split(/\s+/).length : 0
  })

  // Initialisation des voix (Nécessaire pour Chrome/Linux)
  const initVoices = () => { window.speechSynthesis.getVoices(); };
  initVoices();
  if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = initVoices;
  }

  // Gestion Clic Droit pour traduction
  const editorArea = document.querySelector('.ql-editor')
  editorArea.addEventListener('contextmenu', async (e) => {
    e.preventDefault()
    const range = quill.getSelection()
    let word = ""
    if (range && range.length > 0) {
      word = quill.getText(range.index, range.length).trim()
    }
    if (word && word.length > 1) {
      selectedWord.value = word
      lookupResult.value = "Anadihadiana..."
      menuX.value = e.clientX
      menuY.value = e.clientY
      showContextMenu.value = true
      try {
        const res = await axios.get(`http://127.0.0.1:8000/translate/${word}`)
        lookupResult.value = res.data.definition
      } catch (err) { lookupResult.value = "Tsy hita ny famaritana." }
    }
  })

  window.addEventListener('click', () => { showContextMenu.value = false })
})

// FONCTION ANALYSE
const check = async () => {
  const text = quill.getText()
  if (!text.trim()) return
  isAnalyzing.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/analyze', { text: text })
    if (res.data.status === "modified") {
      correctionsOnly.value = res.data.corrections_only
      fullCorrectedText.value = res.data.full_correction
    } else { correctionsOnly.value = [] }
  } catch (err) { console.error(err) }
  finally { isAnalyzing.value = false }
}

// CORRECTIONS
const applySingleCorrection = (item, index) => {
  const text = quill.getText()
  const escapedOriginal = item.original.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`\\b${escapedOriginal}\\b`)
  const newText = text.replace(regex, item.suggestion)
  quill.setText(newText)
  correctionsOnly.value.splice(index, 1)
}

const applyAll = () => {
  if (fullCorrectedText.value) {
    quill.setText(fullCorrectedText.value)
    correctionsOnly.value = []
  }
}

// GESTION PDF
const triggerImport = () => fileInput.value.click()
const handleImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = async (e) => {
    const typedarray = new Uint8Array(e.target.result)
    try {
      const pdf = await pdfjsLib.getDocument(typedarray).promise
      let fullExtractedText = ""
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i)
        const textContent = await page.getTextContent()
        fullExtractedText += textContent.items.map(s => s.str).join(" ") + "\n"
      }
      quill.setText(fullExtractedText)
    } catch (err) { alert("Erreur lecture PDF") }
  }
  reader.readAsArrayBuffer(file)
}

const exportPDF = () => {
  const element = document.querySelector('.ql-editor')
  const opt = {
    margin: 15,
    filename: 'AI-teny-Export.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }
  html2pdf().from(element).set(opt).save()
}

const speakText = () => {
  window.speechSynthesis.cancel();
  const text = quill.getText().trim();
  if (!text) return;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'fr-FR';
  
  utterance.onstart = () => {
    isSpeaking.value = true;
    // SI CETTE ALERTE S'AFFICHE, TON CODE EST PARFAIT
    console.log("Le navigateur envoie le signal audio...");
  };

  utterance.onerror = (event) => {
    alert("Erreur système audio : " + event.error);
  };

  window.speechSynthesis.speak(utterance);
};
</script>

<style>
.ql-editor { padding: 2.5rem !important; min-height: 450px; font-size: 1.25rem; line-height: 1.8; color: #1e293b; }
.ql-toolbar.ql-snow { border: none !important; border-bottom: 1px solid #f1f5f9 !important; padding: 12px 20px !important; background: #fff; }
.ql-container.ql-snow { border: none !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
</style>