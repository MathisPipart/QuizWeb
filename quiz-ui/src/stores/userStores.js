import { defineStore } from 'pinia';
import router from '@/router';
import api from '@/api';

export const useUserStore = defineStore('userStore', {
	state: () => ({
		token: localStorage.getItem('userToken') || null,
		expiration: localStorage.getItem('userTokenExpiration') || null,
		requestTime: localStorage.getItem('requestTime') || null,
	}),
	actions: {
		async login(password) {
			const response = await api.admin.login({ password });

			if (response.status !== 200) {
				throw new Error('Invalid password');
			}

			this.token = response.data.token;
			this.expiration = response.data.expiration;
			this.requestTime = new Date().getTime();
			localStorage.setItem('userToken', this.token);
			localStorage.setItem('userTokenExpiration', this.expiration);
			localStorage.setItem('requestTime', this.requestTime);
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

			if (new Date().getTime() - this.requestTime > this.expiration * 1000) {
				this.token = null;
				localStorage.removeItem('userToken');
				router.push('/');
			}
		},
	},
});
