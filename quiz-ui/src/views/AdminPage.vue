<!-- <template>
	<div class="admin-page">
		<admin-questions />
		<admin-leaderboard />
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
	};
</script>

<style>
	.admin-page {
		display: flex;
		height: 100vh;
		position: relative;
	}

	.questions-module {
		flex: 7;
		display: flex;
		flex-direction: column;
		overflow-x: auto;
		padding-right: 30%;
		/* Reserve space for the leaderboard */
	}

	.leaderboard-module {
		position: absolute;
		right: 0;
		top: 0;
		height: 100%;
		width: 30%;
		display: flex;
		flex-direction: column;
		overflow-y: auto;
		padding: 20px;
		background-color: #f7f7f7;
		box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
	}
</style> -->

<template>
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
