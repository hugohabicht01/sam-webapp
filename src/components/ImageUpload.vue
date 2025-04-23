<script setup lang="ts">
import { ref, computed } from 'vue';
import { useToast } from 'vue-toastification';

const props = defineProps<{
  disabled: boolean
}>();

const emit = defineEmits<{
  (e: 'image-uploaded', value: string): void
}>();

const toast = useToast();
const isDragging = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const dragClasses = computed(() => {
  return {
    'border-primary-500 bg-primary-50 dark:bg-primary-900/10': isDragging,
    'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500': !isDragging,
    'opacity-50 cursor-not-allowed': props.disabled,
    'cursor-pointer': !props.disabled
  };
});

const handleDragEnter = (e: DragEvent) => {
  if (props.disabled) return;
  e.preventDefault();
  isDragging.value = true;
};

const handleDragLeave = (e: DragEvent) => {
  if (props.disabled) return;
  e.preventDefault();
  isDragging.value = false;
};

const handleDragOver = (e: DragEvent) => {
  if (props.disabled) return;
  e.preventDefault();
};

const handleDrop = (e: DragEvent) => {
  if (props.disabled) return;
  e.preventDefault();
  isDragging.value = false;
  
  const files = e.dataTransfer?.files;
  if (files && files.length > 0) {
    handleFile(files[0]);
  }
};

const triggerFileInput = () => {
  if (props.disabled) return;
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  if (props.disabled) return;
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    handleFile(target.files[0]);
  }
};

const handleFile = (file: File) => {
  if (!file.type.startsWith('image/')) {
    toast.error('Please upload an image file');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    if (e.target?.result) {
      emit('image-uploaded', e.target.result as string);
      toast.success('Image uploaded successfully');
    }
  };
  reader.onerror = () => {
    toast.error('Error reading file');
  };
  reader.readAsDataURL(file);
};
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-5">
    <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upload Image</h2>
    
    <div
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @dragover="handleDragOver"
      @drop="handleDrop"
      @click="triggerFileInput"
      class="border-2 border-dashed rounded-lg p-8 text-center transition-colors duration-300"
      :class="dragClasses"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileChange"
        :disabled="props.disabled"
      />
      
      <div class="flex flex-col items-center">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-12 w-12 text-gray-400 dark:text-gray-500 mb-4" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="1.5" 
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" 
          />
        </svg>
        
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ isDragging ? 'Drop image here' : 'Drag & drop image here' }}
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          or <span class="text-primary-500">click to browse</span>
        </p>
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-2">
          Supports JPG, PNG, GIF formats
        </p>
      </div>
    </div>
  </div>
</template>