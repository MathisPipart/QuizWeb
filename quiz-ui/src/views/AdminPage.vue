<template>
	<div class="admin-title">
		<h1>Admin Dashboard</h1>
		<admin-database @reset="handleReset" />
	</div>
	<div class="admin-page">
		<admin-questions :isLeaderboardHidden="isLeaderboardHidden" ref="adminQuestions" />
		<admin-leaderboard @toggle="toggleLeaderboard" ref="adminLeaderboard" />
	</div>
</template>

<script>
import AdminQuestions from "./AdminQuestions.vue";
import AdminLeaderboard from "./AdminLeaderboard.vue";
import AdminDatabase from "../components/AdminDatabase.vue";

export default {
	name: "AdminPage",
	components: {
		AdminQuestions,
		AdminLeaderboard,
		AdminDatabase,
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
		async handleReset() {
			await this.$refs.adminQuestions.fetchQuestions();
			await this.$refs.adminLeaderboard.fetchScores();
		}
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

.admin-title {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20px;
}
</style>