<template>
	<div class="questions-module">
		<div ref="questionsContainer" class="questions-container">
			<div v-for="(question, qIndex) in questions" :key="question.id" class="question-card">
				<div class="question-image">
					<img v-if="question.image" :src="question.image" alt="Question Image" />
				</div>
				<div class="question-content">
					<h2 class="card-title">{{ question.title }}</h2>
					<p class="card-description">{{ question.text }}</p>
					<div class="card-buttons">
						<div class="edit-button-whole">
							<button class="move-left" @click="moveQuestion('left', qIndex)" v-if="qIndex > 0">
								⬅
							</button>
							<button class="card-button" @click="editQuestion(qIndex)"
								:class="{ 'round-left': qIndex == 0, 'round-right': qIndex == questionCount - 1 }">
								Edit
							</button>
							<button class="move-right" @click="moveQuestion('right', qIndex)"
								v-if="qIndex < questionCount - 1">
								⮕
							</button>
						</div>
						<button class="delete-button" @click="confirmDelete(qIndex)">
							<i class="fas fa-trash-alt"></i>
						</button>
					</div>
				</div>
			</div>
			<div class="add-question-card" @click="addQuestion">
				<div class="add-button">+</div>
			</div>
		</div>
		<delete-modal v-if="showDeleteModal" @close="closeDeleteModal" @confirm="deleteQuestion" />
		<question-modal v-if="showEditModal" :question="currentQuestion" @close="closeEditModal" @save="saveQuestion" />
	</div>
</template>

<script>
import DeleteModal from "@/components/DeleteModal.vue";
import QuestionModal from "@/components/QuestionModal.vue";
import api from "@/api";

export default {
	name: "AdminQuestions",
	components: {
		DeleteModal,
		QuestionModal,
	},
	data() {
		return {
			questions: [],
			questionCount: 0,
			showDeleteModal: false,
			showEditModal: false,
			questionToDelete: null,
			currentQuestion: null,
			currentQuestionIndex: null,
		};
	},
	async mounted() {
		await this.fetchQuestions();
	},
	methods: {
		async fetchQuestions() {
			this.questions = [];
			this.questionCount = (await api.quiz.get()).data.size;
			for (let i = 1; i <= this.questionCount; i++) {
				const question = (await api.quiz.question.getByPosition(i)).data;
				question.status = "current"; // Initialize with status 'current'
				this.questions.push(question);
			}
		},
		addQuestion() {
			this.currentQuestion = {
				id: null,
				image: "",
				title: "",
				text: "",
				position: this.questions.length + 1,
				possibleAnswers: [
					{ id: 1, text: "", isCorrect: true },
					{ id: 2, text: "", isCorrect: false },
				],
				status: "new",
			};
			this.showEditModal = true;
		},
		editQuestion(qIndex) {
			this.currentQuestion = { ...this.questions[qIndex] };
			this.currentQuestionIndex = qIndex;
			this.showEditModal = true;
		},
		async saveQuestion(updatedQuestion) {
			if (updatedQuestion.status === "new") {
				this.questions.push(updatedQuestion);
				await this.addQuestionToServer(updatedQuestion);
			} else {
				this.questions.splice(this.currentQuestionIndex, 1, updatedQuestion);
				await this.updateQuestionOnServer(updatedQuestion);
			}
			this.showEditModal = false;
		},
		async addQuestionToServer(question) {
			try {
				const response = await api.admin.question.add(question);
				question.id = response.data.id; // Assume the response contains the new question ID
				question.status = "current";
			} catch (error) {
				console.error("Failed to add question", error);
			}
		},
		async updateQuestionOnServer(question) {
			try {
				await api.admin.question.update(question.id, question);
				question.status = "current";
			} catch (error) {
				console.error("Failed to update question", error);
			}
		},
		confirmDelete(qIndex) {
			this.questionToDelete = qIndex;
			this.showDeleteModal = true;
		},
		closeDeleteModal() {
			this.showDeleteModal = false;
			this.questionToDelete = null;
		},
		async deleteQuestion() {
			const qIndex = this.questionToDelete;
			if (qIndex !== null) {
				const question = this.questions[qIndex];
				if (question.status !== "new") {
					try {
						await api.admin.question.delete(question.id);
					} catch (error) {
						console.error("Failed to delete question", error);
						return;
					}
				}
				this.questions.splice(qIndex, 1);
				this.closeDeleteModal();
			}
		},
		closeEditModal() {
			this.showEditModal = false;
			this.currentQuestion = null;
			this.currentQuestionIndex = null;
		},
		async moveQuestion(direction, qIndex) {
			this.currentQuestion = { ...this.questions[qIndex] };
			if (direction === "left" && qIndex > 0) {
				this.currentQuestion.position -= 1;
				await api.admin.question.update(this.currentQuestion.id, this.currentQuestion);
				await this.fetchQuestions();
			} else if (direction === "right" && qIndex < this.questionCount - 1) {
				this.currentQuestion.position += 1;
				await api.admin.question.update(this.currentQuestion.id, this.currentQuestion);
				await this.fetchQuestions();
			}
		},
	},
};
</script>

<style scoped>
.questions-container {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
	gap: 20px 20px;
	/* Reduce vertical and horizontal gap between grid items */
	overflow-y: auto;
	padding: 20px;
	box-sizing: border-box;
}

.question-card {
	background-color: var(--color-background-soft);
	border-radius: 5px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	overflow: hidden;
	transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	display: flex;
	flex-direction: column;
	height: 300px;
	/* Fixed height for the question cards */
}

.question-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.question-image img {
	width: 100%;
	height: 150px;
	/* Fixed height for the image */
	object-fit: cover;
}

.question-content {
	padding: 10px;
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
}

.card-title {
	font-size: 20px;
	/* Reduce font size */
	margin: 5px 0;
	/* Reduce margin */
}

.card-description {
	font-size: 14px;
	color: var(--color-text-muted);
	margin-bottom: 10px;
	height: 50px;
	overflow-y: auto;
}

.card-buttons {
	display: flex;
	justify-content: space-between;
}

.edit-button-whole {
	display: flex;
	align-items: center;
	width: calc(50% - 5px);
}

.card-button {
	width: 100%;
	display: block;
	padding: 5px;
	text-align: center;
	background-color: var(--vt-c-tertiary);
	color: var(--vt-c-accent-text);
	border: none;
	cursor: pointer;
}

.round-left {
	border-radius: 5px 0 0 5px;
}

.round-right {
	border-radius: 0 5px 5px 0;
}

.card-button:hover {
	background-color: var(--vt-c-tertiary-light);
}

.move-left,
.move-right {
	width: calc(50% - 5px);
	display: block;
	padding: 5px;
	text-align: center;
	background-color: var(--vt-c-primary);
	color: var(--vt-c-accent-text);
	border: none;
	cursor: pointer;
}

.move-left:hover,
.move-right:hover {
	background-color: var(--vt-c-primary-light);
}

.move-left {
	border-radius: 5px 0 0 5px;
}

.move-right {
	border-radius: 0 5px 5px 0;
}

.delete-button {
	display: block;
	width: calc(50% - 5px);
	padding: 5px;
	/* Reduce padding */
	text-align: center;
	background-color: var(--vt-c-important);
	color: var(--vt-c-accent-text);
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.delete-button i {
	color: var(--vt-c-accent-text);
}

.delete-button:hover {
	background-color: var(--vt-c-important-light);
}

.add-question-card {
	display: flex;
	align-items: center;
	justify-content: center;
	height: 300px;
	/* Same fixed height as the question cards */
	background-color: var(--color-background-soft);
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	border-radius: 5px;
	cursor: pointer;
	transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.add-question-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.add-button {
	font-size: 2em;
	color: var(--color-text-muted);
}
</style>