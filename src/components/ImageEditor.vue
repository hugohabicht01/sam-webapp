<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useToast } from "vue-toastification";
import axios from "axios";

const props = defineProps<{
    imageSrc: string;
}>();

const emit = defineEmits<{
    (e: "processed-image", value: string): void;
    (e: "processing", value: boolean): void;
}>();

const toast = useToast();
const imageRef = ref<HTMLImageElement | null>(null);
const isLoading = ref(false);
const showTarget = ref(false);
const targetPosition = ref({ x: 0, y: 0 });
const apiUrl = ref("http://localhost:8000/segment");
const scale = ref(1);
const imageContainerRef = ref<HTMLDivElement | null>(null);

// Load image and set up dimensions on mount or when image changes
onMounted(() => {
    if (imageRef.value && props.imageSrc) {
        imageRef.value.src = props.imageSrc;
    }
});

// Watch for image source changes
watch(
    () => props.imageSrc,
    () => {
        if (imageRef.value) {
            imageRef.value.src = props.imageSrc;
        }
    },
);

// Calculate scale when image is loaded
function handleImageLoad() {
    if (!imageRef.value || !imageContainerRef.value) return;

    // Get container dimensions
    const containerWidth = imageContainerRef.value.clientWidth;
    const containerHeight = imageContainerRef.value.clientHeight;

    // Calculate scale based on container and image size
    const widthScale = containerWidth / imageRef.value.naturalWidth;
    const heightScale = containerHeight / imageRef.value.naturalHeight;
    scale.value = Math.min(widthScale, heightScale, 1);
}

// Handle click on the image
async function handleImageClick(event: MouseEvent) {
    if (isLoading.value || !imageRef.value) return;

    const rect = imageRef.value.getBoundingClientRect();

    // Calculate click position relative to image
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Store target position for display
    targetPosition.value = { x, y };
    showTarget.value = true;

    // Convert displayed image coordinates to original image coordinates
    const originalX = Math.round(x / scale.value);
    const originalY = Math.round(y / scale.value);

    // Process the image with the selected point
    await processImage(originalX, originalY);
}

// Send image and coordinates to the server for processing
async function processImage(x: number, y: number) {
    if (!imageRef.value) return;

    try {
        isLoading.value = true;
        emit("processing", true);

        // Create payload
        const payload = {
            image: props.imageSrc,
            point: { x, y },
        };

        // Send to server
        const response = await axios.post(apiUrl.value, payload, {
            headers: {
                "Content-Type": "application/json",
            },
            responseType: "blob",
        });

        // Convert response blob to base64
        const reader = new FileReader();
        reader.onloadend = () => {
            const base64data = reader.result as string;
            emit("processed-image", base64data);
            showTarget.value = false;
            isLoading.value = false;
            emit("processing", false);
        };
        reader.readAsDataURL(response.data);
    } catch (error) {
        console.error("Error processing image:", error);
        toast.error("Error processing image. Please try again.");
        isLoading.value = false;
        emit("processing", false);
        showTarget.value = false;
    }
}
</script>

<template>
    <div class="relative h-full w-full">
        <div
            ref="imageContainerRef"
            class="relative flex items-center justify-center h-full w-full overflow-hidden bg-gray-100 dark:bg-gray-700"
        >
            <img
                ref="imageRef"
                :src="imageSrc"
                @click="handleImageClick"
                @load="handleImageLoad"
                :class="{
                    'cursor-crosshair': !isLoading,
                    'cursor-wait': isLoading,
                }"
                class="max-w-full max-h-full object-contain transition-opacity duration-300"
                alt="Image for editing"
            />

            <!-- Target indicator -->
            <div
                v-if="showTarget"
                class="absolute pointer-events-none"
                :style="{
                    left: `${targetPosition.x}px`,
                    top: `${targetPosition.y}px`,
                    transform: 'translate(-50%, -50%)',
                }"
            >
                <div class="relative">
                    <div
                        class="w-6 h-6 rounded-full border-2 border-primary-500 flex items-center justify-center"
                    >
                        <div class="w-2 h-2 bg-primary-500 rounded-full"></div>
                    </div>
                    <div
                        v-if="isLoading"
                        class="w-10 h-10 rounded-full border-2 border-primary-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-ping-slow opacity-75"
                    ></div>
                </div>
            </div>

            <!-- Loading overlay -->
            <div
                v-if="isLoading"
                class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center"
            >
                <div class="loader"></div>
                <span class="ml-3 text-white font-medium">Processing...</span>
            </div>

            <!-- Instructions overlay -->
            <div
                v-if="!isLoading && !showTarget"
                class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-70 text-white px-4 py-2 rounded-full text-sm"
            >
                Click on an area to anonymize
            </div>
        </div>
    </div>
</template>
