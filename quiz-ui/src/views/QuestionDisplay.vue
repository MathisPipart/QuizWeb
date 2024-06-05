<script>
export default {
props: {
  currentQuestion: {
    type: Object,
    required: true
  }
},
data() {
  return {
    selectedOption: null
  };
},
methods: {
  handleOptionClick(index) {
    if (this.selectedOption === null) {
      this.selectedOption = index;
      this.$emit('click-on-answer', index);
    }
  }
},
watch: {
  currentQuestion() {
    this.selectedOption = null;
  }
}
}
</script>


<template>
  <h2>{{ currentQuestion.text }}</h2>
  <div class="image-container" v-if="currentQuestion.image">
    <img :src="currentQuestion.image" alt="Question image" class="question-image">
  </div>
  <div class="options-container">
    <div
      class="question-option"
      v-for="(option, index) in currentQuestion.options"
      :key="index"
      @click="handleOptionClick(index)"
      :class="{
        correct: selectedOption === index && option === currentQuestion.correctAnswer,
        incorrect: selectedOption === index && option !== currentQuestion.correctAnswer
      }"
    >
      {{ option }}
    </div>
  </div>
</template>


<style scoped>
.image-container {
width: 100%;
height: 300px;
display: flex;
justify-content: center;
align-items: center;
margin-bottom: 20px;
overflow: hidden;
}

.question-image {
width: 100%;
height: 100%;
object-fit: cover;
object-position: center;
}

.options-container {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 0.5rem;
max-width: 100%;
}

.question-option {
cursor: pointer;
padding: 1rem;
background-color: #2e62af;
border-radius: 5px;
transition: background-color 0.3s;
text-align: center;
}

.question-option:hover {
background-color: rgba(46, 98, 175, 0.56);
}

.question-option.correct {
background-color: #28a745;
}

.question-option.incorrect {
background-color: #dc3545;
}
</style>
