<template>
	<div class="leaderboard-module">
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
		<button @click="confirmResetLeaderboard" class="reset-button">Reset Leaderboard</button>
		<reset-modal v-if="showResetModal" @close="closeResetModal" @confirm="resetLeaderboard" />
	</div>
</template>

<script>
import ResetModal from '@/components/ResetModal.vue';
import api from '@/api';

export default {
	name: 'AdminLeaderboard',
	components: {
		ResetModal
	},
	data() {
		return {
			showResetModal: false,
			scores: [],
			questionCount: 0,
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
		}
	}
};
</script>

<style scoped>
.leaderboard-module {
	position: absolute;
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
}

.scoreboard {
	flex-grow: 1;
	overflow-y: auto;
	margin-bottom: 20px;
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
}

.reset-button:hover {
	background-color: #f76a6a;
}
</style>