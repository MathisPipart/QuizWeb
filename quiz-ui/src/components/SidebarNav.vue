<template>
	<div>
		<div :class="['sidebar', { collapsed: isCollapsed, overlay: isOverlay, visible: isVisible }]">
			<router-link to="/" class="no-hover">
				<img src="/src/assets/logo.png" alt="Quiz Logo" class="logo-image" />
			</router-link>

			<nav v-if="!isCollapsed">
				<router-link to="/" class="to-top user">Home</router-link>
				<div class="spacer"></div>
				<a @click="signOut" v-if="store.token" class="to-bottom user">Sign Out</a>
				<a @click="openLogin" class="to-bottom admin" :class="{ selected: isInAdmin }">Admin</a>
			</nav>

			<AdminLogin v-if="isLogin" @close="closeLogin" class="modal" />
		</div>

		<!-- Floating Toggle Button -->
		<div class="toggle-btn floating" @click="toggleSidebar">
			<span v-if="isCollapsed || isOverlay">☰</span>
			<span v-else>☰</span>
		</div>
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
			isCollapsed: false,
			isOverlay: false,
			isVisible: true,
		};
	},
	components: {
		AdminLogin,
	},
	computed: {
		isInAdmin() {
			return this.$route.path.startsWith('/admin');
		},
	},
	methods: {
		toggleSidebar() {
			if (this.isOverlay) {
				this.isVisible = !this.isVisible;
			} else {
				this.isCollapsed = !this.isCollapsed;
			}
			this.$emit('toggle', { isCollapsed: this.isCollapsed, isOverlay: this.isOverlay });
		},
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
		updateSidebarVisibility() {
			this.isOverlay = window.innerWidth < 768; // Adjust the breakpoint as needed
			this.isVisible = window.innerWidth >= 768;
		},
	},
	mounted() {
		window.addEventListener('resize', this.updateSidebarVisibility);
		this.updateSidebarVisibility();
	},
	beforeUnmount() {
		window.removeEventListener('resize', this.updateSidebarVisibility);
	},
};
</script>


<style scoped>
.sidebar {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 1rem;
	width: 250px;
	/* Fixed size */
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	height: 100vh;
	z-index: 1;
	background-color: var(--color-background-soft);
	position: fixed;
	left: 0;
	top: 0;
	transition: transform 0.3s ease, width 0.3s ease;
}

.collapsed {
	width: 50px;
}

.overlay {
	transform: translateX(-100%);
	position: absolute;
	z-index: 2;
}

.overlay.visible {
	transform: translateX(0);
}

.sidebar.collapsed nav,
.sidebar.collapsed .logo {
	display: none;
}

.logo-image {
	margin: 40px 0;
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
	color: var(--vt-c-accent-text);
	cursor: pointer;
}

nav .router-link-exact-active {
	font-weight: bold;
}

nav .selected {
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
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
	border-radius: 5px;
}

.admin:hover {
	background-color: var(--vt-c-important-light);
	color: var(--vt-c-accent-text);
}

.user {
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	border-radius: 5px;
}

.user:hover {
	background-color: var(--vt-c-primary-light);
	color: var(--vt-c-accent-text);
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

/* Updated styles for the toggle button */
.toggle-btn {
	cursor: pointer;
	align-self: flex-end;
	background: var(--color-background-soft);
	border: 1px solid var(--color-border);
	border-radius: 50%;
	width: 50px;
	/* Fixed width and height for a perfect circle */
	height: 50px;
	/* Fixed width and height for a perfect circle */
	padding: 10;
	box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
	user-select: none;
	/* Make text non-selectable */
	display: flex;
	justify-content: center;
	align-items: center;
}

.toggle-btn span {
	font-size: 1.5rem;
	display: block;
	user-select: none;
	/* Ensure text is non-selectable */
}

.floating {
	position: fixed;
	top: 10px;
	left: 10px;
	z-index: 3;
	cursor: pointer;
}

@media (max-width: 768px) {
	.sidebar {
		transform: translateX(-100%);
		width: 250px;
		/* Maintain width for collapsed state */
	}

	.sidebar.visible {
		transform: translateX(0);
	}
}
</style>