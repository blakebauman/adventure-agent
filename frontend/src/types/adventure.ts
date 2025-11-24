export interface UserPreferences {
  region?: string;
  activity_type?: string;
  duration_days?: number;
  skill_level?: string;
  accommodation_preference?: string;
  group_size?: number;
  dates?: string[];
  distance_preference?: string;
  route_type?: string;
  gear_owned?: string[];
}

export interface AdventurePlan {
  title?: string;
  description?: string;
  itinerary?: any;
  trails?: any[];
  weather_info?: any;
  gear_recommendations?: any[];
  accommodation_info?: any[];
  [key: string]: any;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  adventurePlan?: AdventurePlan;
}

export interface StreamEvent {
  event: string;
  name?: string;
  data?: {
    output?: any;
    [key: string]: any;
  };
  [key: string]: any;
}

export interface RunState {
  status: 'pending' | 'success' | 'error';
  values?: {
    adventure_plan?: AdventurePlan;
    [key: string]: any;
  };
  error?: string;
}

