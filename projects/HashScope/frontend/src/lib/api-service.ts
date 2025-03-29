import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export interface APIKey {
  key_id: string;
  name: string;
  is_active: boolean;
  created_at: string;
  expires_at: string;
  rate_limit_per_minute: number;
  call_count: number;
  last_used_at: string;
}

export interface CreateAPIKeyRequest {
  name?: string;
  rate_limit_per_minute?: number;
}

export interface CreateAPIKeyResponse extends Omit<APIKey, 'call_count' | 'last_used_at'> {
  secret_key: string;
}

export interface APICatalogItem {
  path: string;
  method: string;
  summary: string;
  description: string;
  category: string;
  tags: string[];
}

export interface APICatalogResponse {
  total_count: number;
  apis: APICatalogItem[];
}

export interface APICategoriesResponse {
  [key: string]: string;
}

const apiService = {
  async listAPIKeys(): Promise<APIKey[]> {
    const response = await axios.get(`${API_BASE_URL}/api-keys/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.data;
  },

  async createAPIKey(data: CreateAPIKeyRequest): Promise<CreateAPIKeyResponse> {
    const response = await axios.post(`${API_BASE_URL}/api-keys/`, data, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.data;
  },

  async listAPICatalog(category?: string): Promise<APICatalogResponse> {
    const response = await axios.get(`${API_BASE_URL}/api-catalog/list`, {
      params: { category },
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.data;
  },

  async listAPICategories(): Promise<APICategoriesResponse> {
    const response = await axios.get(`${API_BASE_URL}/api-catalog/categories`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    return response.data;
  },
};

export default apiService;