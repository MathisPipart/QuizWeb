<template>
	<link rel="stylesheet" href="https://use.typekit.net/ocu3dtf.css">
	<div class="app" :class="[{ 'sidebar-overlay': isSidebarOverlay }, sidebarClass]">
		<sidebar-nav :class="{ 'visible': isSidebarVisible && isSidebarOverlay }" @toggle="handleSidebarToggle" />
		<div class="content">
			<router-view />
		</div>
	</div>
</template>

<script>
import { onBeforeMount, ref, computed } from "vue";
import { useUserStore } from "@/stores/userStores";

export default {
	setup() {
		const store = useUserStore();
		const isSidebarVisible = ref(true);
		const isSidebarCollapsed = ref(false);
		const windowWidth = ref(window.innerWidth);

		const isSidebarOverlay = computed(() => windowWidth.value < 768);

		const sidebarClass = computed(() => {
			if (isSidebarOverlay.value) {
				return '';
			} else if (isSidebarCollapsed.value) {
				return 'sidebar-collapsed';
			} else {
				return 'sidebar-expanded';
			}
		});

		const toggleSidebarVisibility = () => {
			isSidebarVisible.value = !isSidebarVisible.value;
		};

		const updateWindowWidth = () => {
			windowWidth.value = window.innerWidth;
			isSidebarVisible.value = window.innerWidth >= 768; // Sidebar should be visible on larger screens by default
		};

		const handleSidebarToggle = ({ isCollapsed, isOverlay }) => {
			isSidebarCollapsed.value = isCollapsed && !isOverlay;
		};

		onBeforeMount(() => {
			store.fetchUser();
		});

		window.addEventListener('resize', updateWindowWidth);

		return {
			store,
			isSidebarVisible,
			toggleSidebarVisibility,
			isSidebarOverlay,
			sidebarClass,
			handleSidebarToggle,
		};
	},
	methods: {
		async periodicFetchUser() {
			await this.store.fetchUser();
		}
	},
	mounted() {
		setInterval(this.periodicFetchUser, 1000 * 60);
	},
	beforeUnmount() {
		window.removeEventListener('resize', this.updateWindowWidth);
	}
};
</script>

<style scoped>
body {
	font-family: "gamay", sans-serif;
	font-weight: 400;
	font-style: normal;
}

.app {
	display: flex;
	min-height: 100vh;
	position: relative;
}

.content {
	flex: 1;
	margin-left: 250px;
	/* Default space for expanded sidebar */
	transition: margin-left 0.3s ease;
}

.sidebar-expanded .content {
	margin-left: 250px;
}

.sidebar-collapsed .content {
	margin-left: 50px;
}

.sidebar-overlay .content {
	margin-left: 0;
	/* No margin for overlay mode */
}

@media (max-width: 768px) {
	.content {
		margin-left: 0;
	}
}
</style>