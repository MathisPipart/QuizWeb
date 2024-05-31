<template>
  <div class="question-display">
    <h2>{{ currentQuestion.text }}</h2>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" class="question-image">
    <div class="options-container">
      <div
        class="question-option"
        v-for="(option, index) in currentQuestion.options"
        :key="index"
        @click="handleOptionClick(option)"
        :class="{
          correct: selectedOption === option && option === currentQuestion.correctAnswer,
          incorrect: selectedOption === option && option !== currentQuestion.correctAnswer
        }"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

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
    handleOptionClick(option) {
      if (!this.selectedOption) {
        this.selectedOption = option;
        this.$emit('click-on-answer', option);
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

<style scoped>
.question-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
}

.options-container {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 2 colonnes */
  gap: 0.5rem;
  max-width: 100%; /* Pour s'ajuster à la largeur de l'image */
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
  background-color: rgba(46, 98, 175, 0.56); /* Moins visible que #2e62af */
}

.question-option.correct {
  background-color: #28a745; /* Vert pour les réponses correctes */
}

.question-option.incorrect {
  background-color: #dc3545; /* Rouge pour les réponses incorrectes */
}
</style>
