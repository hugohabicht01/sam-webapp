import axios from 'axios';
import { SegmentRequest } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const segmentImage = async (request: SegmentRequest): Promise<Blob> => {
  try {
    const response = await api.post('/segment', request, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error) {
    console.error('Error segmenting image:', error);
    throw error;
  }
};

export default api;