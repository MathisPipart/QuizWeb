<template>
	<div class="questions-module">
		<div ref="questionsContainer" class="questions-container">
			<div
				v-for="(question, qIndex) in questions"
				:key="question.id"
				:class="[
					'question-card',
					{
						'new-question': question.status === 'new',
						'edited-question': question.status === 'edited',
					},
				]"
			>
				<div class="question-image">
					<img
						v-if="question.image"
						:src="question.image"
						alt="Question Image"
					/>
					<ImageUploader
						:fileDataUrl="question.image"
						@file-change="(dataUrl) => handleFileChange(dataUrl, qIndex)"
					/>
				</div>
				<div class="question-content">
					<input
						type="text"
						v-model="question.title"
						placeholder="Title"
						@input="markEdited(qIndex)"
					/>
					<textarea
						v-model="question.text"
						placeholder="Question text"
						@input="markEdited(qIndex)"
					></textarea>
					<div
						v-for="(answer, aIndex) in question.possibleAnswers"
						:key="answer.id"
						class="answer"
					>
						<input
							type="text"
							v-model="answer.text"
							placeholder="Answer text"
							@input="markEdited(qIndex)"
						/>
						<input
							type="checkbox"
							v-model="answer.isCorrect"
							@change="
								ensureSingleCorrectAnswer(qIndex, aIndex);
								markEdited(qIndex);
							"
						/>
						Correct
						<button @click="removeAnswer(qIndex, aIndex)">-</button>
					</div>
					<button @click="addAnswer(qIndex)">Add Answer</button>
				</div>
				<div class="question-buttons">
					<button @click="confirmDelete(qIndex)" class="delete-button">
						Delete
					</button>
					<button
						v-if="question.status !== 'current'"
						@click="updateQuestion(qIndex)"
					>
						{{ question.status === "new" ? "Add" : "Update" }}
					</button>
				</div>
			</div>
			<div class="add-question-card" @click="addQuestion">
				<div class="add-button">+</div>
			</div>
		</div>

		<delete-modal
			v-if="showModal"
			@close="closeModal"
			@confirm="deleteQuestion"
		/>
	</div>
</template>

<script>
	import DeleteModal from "@/components/DeleteModal.vue";
	import ImageUploader from "@/components/ImageUploader.vue"; // Import the ImageUploader component
	import api from "@/api";

	export default {
		name: "AdminQuestions",
		components: {
			DeleteModal,
			ImageUploader, // Register the ImageUploader component
		},
		data() {
			return {
				questions: [],
				questionCount: 0,
				showModal: false,
				questionToDelete: null,
			};
		},
		async mounted() {
			this.questionCount = (await api.quiz.get()).data.size;
			for (let i = 1; i <= this.questionCount; i++) {
				const question = (await api.quiz.question.getByPosition(i)).data;
				question.status = "current"; // Initialize with status 'current'
				this.questions.push(question);
			}
		},
		methods: {
			addQuestion() {
				this.questions.push({
					id: this.questions.length + 1,
					image: "",
					title: "",
					text: "",
					position: this.questions.length + 1,
					possibleAnswers: [
						{ id: 1, text: "", isCorrect: false },
						{ id: 2, text: "", isCorrect: false },
					],
					status: "new", // Mark as new
				});
				this.$nextTick(() => {
					const container = this.$refs.questionsContainer;
					container.scrollLeft = container.scrollWidth;
				});
			},
			addAnswer(qIndex) {
				const newAnswerId = this.questions[qIndex].possibleAnswers.length + 1;
				this.questions[qIndex].possibleAnswers.push({
					id: newAnswerId,
					text: "",
					isCorrect: false,
				});
				this.markEdited(qIndex); // Mark as edited when adding an answer
			},
			removeAnswer(qIndex, aIndex) {
				this.questions[qIndex].possibleAnswers.splice(aIndex, 1);
				this.markEdited(qIndex); // Mark as edited when removing an answer
			},
			ensureSingleCorrectAnswer(qIndex, aIndex) {
				this.questions[qIndex].possibleAnswers.forEach((answer, index) => {
					if (index !== aIndex) {
						answer.isCorrect = false;
					}
				});
			},
			markEdited(qIndex) {
				if (this.questions[qIndex].status === "current") {
					this.questions[qIndex].status = "edited";
				}
			},
			async updateQuestion(index) {
				const question = this.questions[index];

				// Remove empty answers
				question.possibleAnswers = question.possibleAnswers.filter(
					(answer) => answer.text.trim() !== ""
				);
				// Ensure there is at least one correct answer
				if (!question.possibleAnswers.some((answer) => answer.isCorrect)) {
					question.possibleAnswers[0].isCorrect = true;
				}

				if (question.status === "new") {
					await api.admin.question.add(question);
				} else if (question.status === "edited") {
					await api.admin.question.update(question.id, question);
				}
				this.questions[index].status = "current"; // Mark as current after saving
			},
			confirmDelete(qIndex) {
				this.questionToDelete = qIndex;
				this.showModal = true;
			},
			closeModal() {
				this.showModal = false;
				this.questionToDelete = null;
			},
			async deleteQuestion() {
				const qIndex = this.questionToDelete;
				if (qIndex !== null) {
					const question = this.questions[qIndex];
					if (question.status !== "new") {
						await api.admin.question.delete(question.id);
					}
					this.questions.splice(qIndex, 1);
					this.closeModal();
				}
			},
			async fetchQuestions() {
				this.questions = [];
				for (let i = 1; i <= this.questionCount; i++) {
					const question = (await api.quiz.question.get(i)).data;
					question.status = "current"; // Initialize with status 'current'
					this.questions.push(question);
				}
			},
			handleFileChange(dataUrl, qIndex) {
				this.questions[qIndex].image = dataUrl;
				this.markEdited(qIndex);
			},
		},
	};
</script>

<style scoped>
	.questions-container {
		display: flex;
		overflow-x: auto;
		overflow-y: hidden;
		padding: 20px;
		height: 100%;
		/* Full height */
	}

	.question-card {
		background-color: #fff;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		border-radius: 10px;
		padding: 20px;
		margin-right: 20px;
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		width: 300px;
		height: 100%;
		/* Ensure cards take full height */
		transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
	}

	.question-card:hover {
		transform: translateY(-5px);
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
	}

	.question-image img {
		width: 100%;
		height: auto;
		border-radius: 10px;
	}

	.question-content {
		margin-top: 10px;
		flex-grow: 1;
	}

	.question-content input[type="text"],
	.question-content textarea {
		width: 100%;
		padding: 10px;
		margin-bottom: 10px;
		border: 1px solid #ccc;
		border-radius: 5px;
	}

	.answer {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.answer input[type="text"] {
		width: calc(100% - 60px);
	}

	.answer input[type="checkbox"] {
		margin-left: 10px;
	}

	.answer button {
		padding: 5px 10px;
		background-color: #f94f4f;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		color: white;
	}

	.answer button:hover {
		background-color: #f76a6a;
	}

	.question-buttons {
		display: flex;
		justify-content: space-between;
		margin-top: 10px;
	}

	.question-buttons .delete-button {
		background-color: #f94f4f;
		border: none;
		border-radius: 5px;
		color: white;
		padding: 10px;
		cursor: pointer;
	}

	.question-buttons .delete-button:hover {
		background-color: #f76a6a;
	}

	.question-buttons button {
		padding: 10px 20px;
		background-color: #77dd77;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		color: white;
	}

	.question-buttons button:hover {
		background-color: #90ee90;
	}

	.add-question-card {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 300px;
		height: 100%;
		/* Ensure the add card takes full height */
		background-color: #f2f2f2;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		border-radius: 10px;
		cursor: pointer;
		flex-shrink: 0;
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

	.new-question {
		background-color: #e7f7e7;
	}

	.edited-question {
		background-color: #f7e7e7;
	}
</style>
