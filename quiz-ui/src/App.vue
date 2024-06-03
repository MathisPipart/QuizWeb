<template>

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
};

</script>

<style scoped>
.app {
	display: flex;
	min-height: 100vh;
}

.content {
	flex: 1;
}
</style>