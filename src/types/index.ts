export interface Point {
  x: number;
  y: number;
}

export interface SegmentRequest {
  image: string; // Base64 encoded image
  point: Point;
}

export interface HistoryState {
  imageData: string;
  timestamp: number;
}