import { defineStore } from 'pinia';
import router from '@/router';
import api from '@/api';

export const useUserStore = defineStore('userStore', {
	state: () => ({
		token: localStorage.getItem('userToken') || null,
		expiration: localStorage.getItem('userTokenExpiration') || null,
	}),
	actions: {
		async login(password) {
			const response = await api.admin.login({ password });

			if (response.status !== 200) {
				throw new Error('Invalid password');
			}

			this.token = response.data.token;
			this.expiration = response.data.expiration;
			localStorage.setItem('userToken', this.token);
			localStorage.setItem('userTokenExpiration', this.expiration);
			router.push('/admin');
		},
		async logout() {
			this.token = null;
			localStorage.removeItem('userToken');
			router.push('/');
		},
		async fetchUser() {
			if (!this.token) {
				router.push('/');
			}

			const response = await api.admin.checkLogin();
			if (response.status !== 200) {
				this.token = null;
				localStorage.removeItem('userToken');
				router.push('/');
			}
		},
	},
});
