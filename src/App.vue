<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ImageUpload from './components/ImageUpload.vue';
import ImageEditor from './components/ImageEditor.vue';
import ControlPanel from './components/ControlPanel.vue';
import { useToast } from 'vue-toastification';

// State
const isProcessing = ref(false);
const currentImageIndex = ref(-1);
const imageHistory = ref<string[]>([]);
const toast = useToast();

// Methods
const handleImageUpload = (imageData: string) => {
  // Clear history when uploading a new image
  imageHistory.value = [imageData];
  currentImageIndex.value = 0;
};

const addToHistory = (imageData: string) => {
  // Remove any forward history when adding a new state
  if (currentImageIndex.value < imageHistory.value.length - 1) {
    imageHistory.value = imageHistory.value.slice(0, currentImageIndex.value + 1);
  }
  
  imageHistory.value.push(imageData);
  currentImageIndex.value = imageHistory.value.length - 1;
};

const handleUndo = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  } else {
    toast.info("Already at the beginning of history");
  }
};

const handleRedo = () => {
  if (currentImageIndex.value < imageHistory.value.length - 1) {
    currentImageIndex.value++;
  } else {
    toast.info("Already at the latest change");
  }
};

const handleReset = () => {
  if (imageHistory.value.length > 0) {
    imageHistory.value = [imageHistory.value[0]];
    currentImageIndex.value = 0;
    toast.success("Image reset to original");
  }
};

const handleDownload = () => {
  if (imageHistory.value.length === 0 || currentImageIndex.value < 0) {
    toast.error("No image to download");
    return;
  }

  const link = document.createElement('a');
  link.href = imageHistory.value[currentImageIndex.value];
  link.download = 'anonymized-image.png';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  toast.success("Image downloaded successfully");
};

const setProcessing = (value: boolean) => {
  isProcessing.value = value;
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm py-4">
      <div class="container mx-auto px-4">
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Image Anonymizer</h1>
        <p class="text-sm text-gray-600 dark:text-gray-300">Securely anonymize sensitive areas in your images</p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-6 flex flex-col md:flex-row gap-6">
      <!-- Left Column: Upload & Controls -->
      <div class="w-full md:w-1/3 space-y-6">
        <ImageUpload 
          @image-uploaded="handleImageUpload" 
          :disabled="isProcessing"
        />
        
        <ControlPanel
          :can-undo="currentImageIndex > 0"
          :can-redo="currentImageIndex < imageHistory.length - 1"
          :has-image="imageHistory.length > 0"
          :is-processing="isProcessing"
          @undo="handleUndo"
          @redo="handleRedo"
          @reset="handleReset"
          @download="handleDownload"
        />
      </div>
      
      <!-- Right Column: Image Editor -->
      <div class="w-full md:w-2/3 bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-hidden">
        <ImageEditor
          v-if="imageHistory.length > 0 && currentImageIndex >= 0"
          :image-src="imageHistory[currentImageIndex]"
          @processed-image="addToHistory"
          @processing="setProcessing"
        />
        <div v-else class="h-96 flex items-center justify-center text-gray-400 dark:text-gray-600">
          <p class="text-lg">Upload an image to begin</p>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white dark:bg-gray-800 py-4 mt-auto">
      <div class="container mx-auto px-4 text-center text-sm text-gray-600 dark:text-gray-400">
        <p>Image Anonymizer &copy; 2025. All images are processed securely and not stored on our servers.</p>
      </div>
    </footer>
  </div>
</template>