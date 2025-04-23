<script setup lang="ts">
const props = defineProps<{
  canUndo: boolean;
  canRedo: boolean;
  hasImage: boolean;
  isProcessing: boolean;
}>();

const emit = defineEmits<{
  (e: 'undo'): void;
  (e: 'redo'): void;
  (e: 'reset'): void;
  (e: 'download'): void;
}>();
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-5">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Controls</h2>
    
    <div class="space-y-3">
      <!-- History Controls -->
      <div class="flex gap-2">
        <button
          @click="emit('undo')"
          :disabled="!canUndo || isProcessing"
          class="flex-1 py-2 px-4 rounded-md bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div class="flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Undo
          </div>
        </button>
        <button
          @click="emit('redo')"
          :disabled="!canRedo || isProcessing"
          class="flex-1 py-2 px-4 rounded-md bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div class="flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
            Redo
          </div>
        </button>
      </div>
      
      <!-- Action Buttons -->
      <button
        @click="emit('reset')"
        :disabled="!hasImage || isProcessing"
        class="w-full py-2 px-4 rounded-md bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 font-medium transition-colors duration-200 hover:bg-gray-100 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <div class="flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Reset
        </div>
      </button>
      
      <button
        @click="emit('download')"
        :disabled="!hasImage || isProcessing"
        class="w-full py-2 px-4 rounded-md bg-primary-600 text-white font-medium transition-colors duration-200 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <div class="flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Download
        </div>
      </button>
    </div>
    
    <div class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div class="text-xs text-gray-500 dark:text-gray-400">
        <p class="mb-1"><strong>How to use:</strong></p>
        <ol class="list-decimal list-inside space-y-1">
          <li>Upload an image using drag &amp; drop or the file picker</li>
          <li>Click on any area you want to anonymize</li>
          <li>Use Undo/Redo to navigate through your changes</li>
          <li>Download the final anonymized image</li>
        </ol>
      </div>
    </div>
  </div>
</template>