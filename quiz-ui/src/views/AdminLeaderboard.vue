<template>
	<div>
		<button class="show-leaderboard-button" @click="toggleLeaderboard">
			{{ isLeaderboardHidden ? "Show Leaderboard" : "Hide Leaderboard" }}
		</button>
		<div :class="['leaderboard-module', { hidden: isLeaderboardHidden }]">
			<h2>Leaderboard</h2>
			<div class="scoreboard">
				<div v-for="(score, index) in scores" :key="score.playerName" :class="{
					first: index === 0,
					second: index === 1,
					third: index === 2,
					other: index >= 3,
				}">
					<span class="position">{{ index + 1 }}</span>
					<span class="name">{{ score.playerName }}</span>
					<span class="score">{{ score.score }} / {{ questionCount }}</span>
				</div>
			</div>
			<button @click="confirmResetLeaderboard" class="reset-button">
				Reset Leaderboard
			</button>
			<reset-modal v-if="showResetModal" @close="closeResetModal" @confirm="resetLeaderboard" />
		</div>
	</div>
</template>

<script>
import ResetModal from "@/components/ResetModal.vue";
import api from "@/api";

export default {
	name: "AdminLeaderboard",
	components: {
		ResetModal,
	},
	data() {
		return {
			showResetModal: false,
			scores: [],
			questionCount: 0,
			isLeaderboardHidden: true, // Hidden by default
		};
	},
	async mounted() {
		const data = (await api.quiz.get()).data;

		this.scores = data.scores;
		this.scores.sort((a, b) => b.score - a.score);
		this.questionCount = data.size;
	},
	methods: {
		confirmResetLeaderboard() {
			this.showResetModal = true;
		},
		closeResetModal() {
			this.showResetModal = false;
		},
		async fetchScores() {
			const data = (await api.quiz.get()).data;

			this.scores = data.scores;
			this.scores.sort((a, b) => b.score - a.score);
			this.questionCount = data.size;
		},
		async resetLeaderboard() {
			await api.admin.participation.deleteAll();
			await this.fetchScores();
			this.closeResetModal();
		},
		toggleLeaderboard() {
			this.isLeaderboardHidden = !this.isLeaderboardHidden;
			this.$emit("toggle", this.isLeaderboardHidden);
		},
	},
};
</script>

<style scoped>
.leaderboard-module {
	position: fixed;
	right: 0;
	top: 0;
	height: 100%;
	width: 30%;
	display: flex;
	flex-direction: column;
	padding: 20px;
	background-color: #f7f7f7;
	box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
	border-left: 1px solid #ccc;
	box-sizing: border-box;
	transition: transform 0.3s ease;
	transform: translateX(100%);
	/* Hidden by default */
}

.leaderboard-module.hidden {
	transform: translateX(100%);
}

.leaderboard-module:not(.hidden) {
	transform: translateX(0);
}

.show-leaderboard-button {
	position: fixed;
	bottom: 10px;
	right: 10px;
	background-color: #007bff;
	color: white;
	border: none;
	padding: 10px;
	cursor: pointer;
	z-index: 1;
	border-radius: 5px;
}

.show-leaderboard-button:hover {
	background-color: #0056b3;
}

.close-button {
	position: absolute;
	top: 10px;
	right: 10px;
	background-color: transparent;
	border: none;
	font-size: 24px;
	cursor: pointer;
	z-index: 1000;
}

.scoreboard {
	flex-grow: 1;
	overflow-y: auto;
	padding: 0;
	margin: 0 0;
}

.leaderboard-item {
	padding: 10px;
	border-bottom: 1px solid #ccc;
}

.reset-button {
	padding: 10px 20px;
	background-color: #f94f4f;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	align-self: flex-end;
	position: fixed;
	bottom: 10px;
	left: 10px;
}

.reset-button:hover {
	background-color: #f76a6a;
}
</style>