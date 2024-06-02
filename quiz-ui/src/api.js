import axios from "axios";

const axiosInstance = axios.create({
	baseURL: "http://127.0.0.1:5000",
});

const api = {
	quiz: {
		get() {
			return axiosInstance.get("/quiz-info");
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
				return axiosInstance.post("/participation", data);
			}
		}
	},
	admin: {
		login(data) {
			return axiosInstance.post("/login", data);
		},
		question: {
			add(data) {
				return axiosInstance.post("/question", data);
			},
			delete(id) {
				return axiosInstance.delete(`/question/${id}`);
			},
			deleteAll() {
				return axiosInstance.delete("/question/all");
			},
			update(id, data) {
				return axiosInstance.put(`/question/${id}`, data);
			},
		},
		participation: {
			deleteAll() {
				return axiosInstance.delete("/participation/all");
			}
		}
	}
};

export default api;