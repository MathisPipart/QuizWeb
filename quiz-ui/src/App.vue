<template>

	<link rel="stylesheet" href="https://use.typekit.net/ocu3dtf.css">

	<div class="app">

		<sidebar-nav />

		<div class="content">
			<router-view />
		</div>

	</div>

</template>

<script>

import { onBeforeMount } from "vue";
import { useUserStore } from "@/stores/userStores";

export default {
	setup() {
		const store = useUserStore();

		onBeforeMount(() => {
			store.fetchUser();
		});

		return {
			store,
		};
	},
	methods: {
		async periodicFetchUser() {
			await this.store.fetchUser();
		}
	},
	mounted() {
		setInterval(this.periodicFetchUser, 1000 * 60);
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
}

.content {
	flex: 1;
}
</style>