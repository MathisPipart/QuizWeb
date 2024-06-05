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
						<button class="card-button" @click="editQuestion(qIndex)">
							Edit
						</button>
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
	},
};
</script>

<style scoped>
.questions-container {
	display: flex;
	flex-wrap: wrap;
	overflow-y: auto;
	padding: 20px;
	box-sizing: border-box;
	height: 100vh;
}

.question-card {
	width: calc(33.333% - 40px);
	background-color: #fff;
	border-radius: 10px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	margin: 10px;
	overflow: hidden;
	transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	display: flex;
	flex-direction: column;
}

.question-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.question-image img {
	width: 100%;
	height: 200px;
	object-fit: cover;
}

.question-content {
	padding: 20px;
	flex-grow: 1;
}

.card-title {
	font-size: 24px;
	margin: 10px 0;
}

.card-description {
	font-size: 14px;
	color: #555;
	margin-bottom: 20px;
}

.card-buttons {
	display: flex;
	justify-content: space-between;
}

.card-button {
	display: block;
	width: calc(50% - 5px);
	padding: 10px;
	text-align: center;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.card-button:hover {
	background-color: #0056b3;
}

.delete-button {
	display: block;
	width: calc(50% - 5px);
	padding: 10px;
	text-align: center;
	background-color: #f94f4f;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
}

.delete-button i {
	color: white;
}

.delete-button:hover {
	background-color: #f76a6a;
}

.add-question-card {
	display: flex;
	align-items: center;
	justify-content: center;
	width: calc(33.333% - 40px);
	height: 200px;
	background-color: #f2f2f2;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	border-radius: 10px;
	cursor: pointer;
	margin: 10px;
	transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.add-question-card:hover {
	transform: translateY(-5px);
	box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.add-button {
	font-size: 2em;
	color: #aaa;
}
</style>
