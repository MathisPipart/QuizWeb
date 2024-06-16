import axios from 'axios';
import { useUserStore } from '@/stores/userStores';

const axiosInstance = axios.create({
	baseURL: 'http://127.0.0.1:5000',
});

axiosInstance.interceptors.request.use(
	config => {
		const userStore = useUserStore();
		const token = userStore.token;
		if (token) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	error => {
		return Promise.reject(error);
	}
);

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
				return axiosInstance.post('/participations', data);
			}
		}
	},
	admin: {
		login(data) {
			return axiosInstance.post('/login', data);
		},
		checkLogin() {
			return axiosInstance.get('/login');
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
		},
		database: {
			reset() {
				return axiosInstance.post('/rebuild-db');
			},
			init() {
				return axiosInstance.post('/init-db');
			}
		}
	}
};

export default api;
