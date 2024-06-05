<template>
	<div class="admin-title">
		<h1>Admin Dashboard</h1>
	</div>
	<div class="admin-page">
		<admin-questions :isLeaderboardHidden="isLeaderboardHidden" />
		<admin-leaderboard @toggle="toggleLeaderboard" />
	</div>
</template>

<script>
import AdminQuestions from "./AdminQuestions.vue";
import AdminLeaderboard from "./AdminLeaderboard.vue";

export default {
	name: "AdminPage",
	components: {
		AdminQuestions,
		AdminLeaderboard,
	},
	data() {
		return {
			isLeaderboardHidden: true,
		};
	},
	methods: {
		toggleLeaderboard(isHidden) {
			this.isLeaderboardHidden = isHidden;
		},
	},
};
</script>

<style>
.admin-page {
	display: flex;
	height: 100vh;
	position: relative;
}

.questions-module {
	flex: 1;
	display: flex;
	flex-direction: column;
	overflow-x: auto;
	transition: padding-right 0.3s ease;
}

.questions-module.expanded {
	padding-right: 30%;
}

.questions-module.collapsed {
	padding-right: 0;
}
</style>
