<template>

	<div class="database-container">
		<h2>Database Management</h2>
		<div class="database-buttons">
			<button class="empty" @click="clearDatabase">Empty</button>
			<button class="load-default" @click="initDatabase">Load Default</button>
		</div>
	</div>

</template>

<script>

import api from "@/api";

export default {
	name: "AdminDatabase",
	methods: {
		async clearDatabase() {
			await api.admin.database.reset();
			this.$emit("reset");
		},
		async initDatabase() {
			await api.admin.database.init();
			this.$emit("reset");
		},
	},
}

</script>

<style>
.database-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: white;
	border-radius: 5px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	padding: 20px;
}

.database-buttons {
	display: flex;
}

.database-buttons button {
	margin: 10px;
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.database-buttons button.empty {
	background-color: #f94f4f;
	color: white;
}
</style>