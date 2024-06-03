<template>
	<div class="sidebar">
		<router-link to="/" class="no-hover">
			<div class="logo">
				<img src="/src/assets/logo.png" alt="Quiz Logo" class="logo-image" />
			</div>
		</router-link>

		<nav>
			<router-link to="/" class="to-top user">Home</router-link>
			<div class="spacer"></div>
			<a @click="signOut" v-if="store.token" class="to-bottom user">Sign Out</a>
			<a @click="openLogin" class="to-bottom admin">Admin</a>
		</nav>

		<AdminLogin v-if="isLogin" @close="closeLogin" class="modal" />
	</div>
</template>

<script>
import { useUserStore } from '@/stores/userStores';
import AdminLogin from '@/components/AdminLogin.vue';

export default {
	name: 'SidebarNav',
	setup() {
		return {
			store: useUserStore(),
		};
	},
	data() {
		return {
			isLogin: false,
		};
	},
	components: {
		AdminLogin,
	},
	methods: {
		openLogin() {
			if (!this.store.token) {
				this.isLogin = true;
			} else {
				this.$router.push('/admin');
			}
		},
		closeLogin() {
			this.isLogin = false;
		},
		signOut() {
			this.store.logout();
			this.store.fetchUser();
		},
	},
};
</script>

<style>
.sidebar {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 1rem;
	width: 12%;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	height: 100vh;
	z-index: 1;
	background-color: white;
}

.logo {
	margin-bottom: 2rem;
}

.logo-image {
	max-width: 150px;
	height: auto;
}

nav {
	display: flex;
	flex-direction: column;
	width: 100%;
	font-size: 1rem;
	text-align: center;
	flex-grow: 1;
}

nav a {
	display: block;
	padding: 0.5rem 0;
	text-decoration: none;
	color: var(--color-text);
	cursor: pointer;
}

nav .router-link-exact-active {
	font-weight: bold;
}

nav a.to-top {
	margin-bottom: 0;
}

nav a.to-bottom {
	margin-top: auto;
	margin-bottom: 1rem;
}

.admin {
	background-color: #f94f4f;
	color: white;
	border-radius: 5px;
}

.admin:hover {
	background-color: #f76a6a;
	color: white;
}

.user {
	background-color: #77dd77;
	color: white;
	border-radius: 5px;
}

.user:hover {
	background-color: #90ee90;
	color: white;
}

.spacer {
	flex-grow: 1;
}

.modal {
	display: flex;
	justify-content: center;
	align-items: center;
	position: fixed;
	z-index: 2;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgba(0, 0, 0, 0.5);
}

.no-hover:hover {
	background-color: transparent;
}
</style>