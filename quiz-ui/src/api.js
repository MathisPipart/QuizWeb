import axios from 'axios';
import { useUserStore } from '@/stores/userStores';

// Create axios instance
const axiosInstance = axios.create({
	baseURL: 'http://127.0.0.1:5000',
});

// Add a request interceptor to include the Authorization header
axiosInstance.interceptors.request.use(
	config => {
		const userStore = useUserStore();
		const token = userStore.token; // Get the token from the Pinia store
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	error => {
		return Promise.reject(error);
	}
);

// Define the API methods
const api = {
	quiz: {
		get() {
			return axiosInstance.get('/quiz-info');
		},
		question: {
			get(id) {
				return axiosInstance.get(`/questions/${id}`);
			},
			getByPosition(position) {
				return axiosInstance.get(`/questions?position=${position}`);
			}
		},
		participation: {
			add(data) {
				return axiosInstance.post('/participation', data);
			}
		}
	},
	admin: {
		login(data) {
			return axiosInstance.post('/login', data);
		},
		question: {
			add(data) {
				return axiosInstance.post('/questions', data); // Note the endpoint
			},
			delete(id) {
				return axiosInstance.delete(`/questions/${id}`);
			},
			deleteAll() {
				return axiosInstance.delete('/questions/all');
			},
			update(id, data) {
				return axiosInstance.put(`/questions/${id}`, data);
			}
		},
		participation: {
			deleteAll() {
				return axiosInstance.delete('/participations/all');
			}
		}
	}
};

export default api;
