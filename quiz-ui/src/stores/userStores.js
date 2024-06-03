import { defineStore } from 'pinia';
import router from '@/router';
import api from '@/api';

export const useUserStore = defineStore('userStore', {
	state: () => ({
		token: localStorage.getItem('userToken') || null,
	}),
	actions: {
		async login(password) {
			const response = await api.admin.login({ password });

			if (response.status !== 200) {
				throw new Error('Invalid password');
			}

			this.token = response.data.token;
			localStorage.setItem('userToken', this.token);
			router.push('/admin');
		},
		async logout() {
			this.token = null;
			localStorage.removeItem('userToken');
			router.push('/');
		},
		fetchUser() {
			if (!this.token) {
				router.push('/');
			}
		},
	},
});
