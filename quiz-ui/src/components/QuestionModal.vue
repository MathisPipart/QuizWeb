<template>
	<div class="modal-overlay" @click.self="closeModal">
		<div class="modal-content">
			<span class="close-button" @click="closeModal">
				<i class="fas fa-times"></i>
			</span>
			<div class="form-group">
				<label class="form-label">Title:</label>
				<input
					type="text"
					v-model="editableQuestion.title"
					class="form-input"
				/>
			</div>
			<div class="form-group">
				<label class="form-label">Question text:</label>
				<textarea
					v-model="editableQuestion.text"
					class="form-textarea"
				></textarea>
			</div>
			<div class="form-group">
				<label class="form-label">Image:</label>
				<input type="file" @change="uploadImage" class="form-input-file" />
				<img
					v-if="editableQuestion.image"
					:src="editableQuestion.image"
					alt="Question Image"
					class="question-image"
				/>
			</div>
			<div class="answers-container">
				<div
					v-for="(answer, index) in editableQuestion.possibleAnswers"
					:key="index"
					class="answer-edit form-group"
				>
					<label class="form-label answer-label">Answer:</label>
					<div class="answer-row">
						<input
							type="text"
							v-model="answer.text"
							class="form-input answer-input"
						/>
						<label class="correct-label">
							Correct:
							<input
								type="checkbox"
								v-model="answer.isCorrect"
								@change="setCorrectAnswer(index)"
							/>
						</label>
						<button class="delete-button" @click="removeAnswer(index)">
							Supprimer
						</button>
					</div>
				</div>
			</div>
			<div class="button-group">
				<button @click="addAnswer" class="add-answer-button">Add Answer</button>
				<button @click="saveChanges" class="save-button">Save</button>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: "QuestionModal",
		props: {
			question: {
				type: Object,
				required: true,
			},
		},
		data() {
			return {
				editableQuestion: JSON.parse(JSON.stringify(this.question)),
			};
		},
		methods: {
			uploadImage(event) {
				const file = event.target.files[0];
				if (file) {
					const reader = new FileReader();
					reader.onload = (e) => {
						this.editableQuestion.image = e.target.result;
					};
					reader.readAsDataURL(file);
				}
			},
			setCorrectAnswer(index) {
				this.editableQuestion.possibleAnswers.forEach((answer, i) => {
					answer.isCorrect = i === index;
				});
			},
			removeAnswer(index) {
				this.editableQuestion.possibleAnswers.splice(index, 1);
			},
			addAnswer() {
				this.editableQuestion.possibleAnswers.push({
					text: "",
					isCorrect: false,
				});
			},
			saveChanges() {
				this.$emit("save", JSON.parse(JSON.stringify(this.editableQuestion)));
			},
			closeModal() {
				this.$emit("close");
			},
		},
		watch: {
			question: {
				handler(newQuestion) {
					this.editableQuestion = JSON.parse(JSON.stringify(newQuestion));
				},
				deep: true,
				immediate: true,
			},
		},
	};
</script>

<style scoped>
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.modal-content {
		background-color: #fff;
		padding: 20px;
		border-radius: 10px;
		width: 90%;
		max-width: 800px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		position: relative;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
	}

	.close-button {
		position: absolute;
		top: 20px;
		right: 20px;
		font-size: 24px;
		color: #fff;
		background-color: #dc3545;
		border: none;
		border-radius: 50%;
		width: 40px;
		height: 40px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		z-index: 1010;
	}

	.form-group {
		margin-bottom: 20px;
	}

	.form-label {
		display: block;
		margin-bottom: 5px;
		color: #555;
		font-weight: bold;
		text-align: left;
	}

	.form-input,
	.form-textarea,
	.form-input-file {
		width: 100%;
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 5px;
		box-sizing: border-box;
	}

	.form-textarea {
		resize: vertical;
		height: 100px;
	}

	.question-image {
		width: 100%;
		max-height: 200px;
		object-fit: cover;
		margin-top: 10px;
		border-radius: 5px;
	}

	.answers-container {
		padding: 20px;
		display: flex;
		flex-wrap: wrap;
		gap: 20px;
		max-height: 300px;
		overflow-y: auto;
		flex-grow: 1;
	}

	.answer-edit {
		flex: 1 1 calc(50% - 20px);
	}

	.answer-label {
		margin-bottom: 5px;
		text-align: left;
	}

	.answer-row {
		display: flex;
		align-items: center;
	}

	.answer-input {
		flex-grow: 1;
		margin-right: 10px;
	}

	.correct-label {
		display: flex;
		align-items: center;
		margin-right: 10px;
	}

	.delete-button {
		background-color: #dc3545;
		color: white;
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
		cursor: pointer;
	}

	.delete-button:hover {
		background-color: #c82333;
	}

	.button-group {
		display: flex;
		justify-content: space-between;
		gap: 10px;
		margin-top: 20px;
	}

	.add-answer-button {
		flex: 1;
		padding: 15px;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 5px;
		font-size: 18px;
		cursor: pointer;
	}

	.add-answer-button:hover {
		background-color: #0056b3;
	}

	.save-button {
		flex: 1;
		padding: 15px;
		background-color: #28a745;
		color: white;
		border: none;
		border-radius: 5px;
		font-size: 18px;
		cursor: pointer;
	}

	.save-button:hover {
		background-color: #218838;
	}
</style>
