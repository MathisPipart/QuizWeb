<template>
	<div class="whole-admin-page">
		<div class="admin-title">
			<h1>Admin Dashboard</h1>
			<admin-database @reset="handleReset" />
		</div>
		<div class="admin-page">
			<admin-questions class="questions-module" :isLeaderboardHidden="isLeaderboardHidden" ref="adminQuestions" />
			<admin-leaderboard @toggle="toggleLeaderboard" ref="adminLeaderboard" />
		</div>
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
.whole-admin-page {
	height: 100vh;
	display: flex;
	flex-direction: column;
}

.admin-title {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20px;
	flex-shrink: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
	.admin-title {
		flex-direction: column;
		align-items: flex-start;
		/* Align items to the start of the column */
	}

	.admin-title h1 {
		margin-bottom: 10px;
		/* Add some space between the title and the database component */
		width: 100%;
		text-align: center;
		/* Center the text in the column layout */
	}

	.admin-title .database-container {
		width: 100%;
		display: flex;
		flex-grow: 1;
	}
}

.admin-page {
	display: flex;
	flex-direction: column;
	flex-grow: 1;
	/* Takes remaining space available */
	overflow: hidden;
}

.questions-module {
	flex: 1;
	display: flex;
	flex-direction: column;
	overflow-y: auto;
	transition: padding-right 0.3s ease;
}

.questions-module.expanded {
	padding-right: 30%;
}

.questions-module.collapsed {
	padding-right: 0;
}

.admin-leaderboard {
	display: none;
}
</style>
