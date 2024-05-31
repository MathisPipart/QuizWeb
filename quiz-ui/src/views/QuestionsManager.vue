<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from '@/services/ParticipationStorageService';
import QuestionDisplay from '../views/QuestionDisplay.vue';
import ParisImage from '../assets/Paris.jpg';
import PlaneteImage from '../assets/Planete.jpg';

const playerName = ref(participationStorageService.getPlayerName() || 'Player');

const currentQuestion = ref({});
const currentQuestionPosition = ref(0);
const totalNumberOfQuestion = ref(0);
const quizFinished = ref(false);
const score = ref(0);

const registeredScores = ref([
  { playerName: "John", score: 10 },
  { playerName: "Jane", score: 20 },
  { playerName: "Paul", score: 30 },
  { playerName: "Christ", score: 40 },
  { playerName: "Anne", score: 50 },
  { playerName: "Julia", score: 60 },
  
]);

const questions = [ 
    { 
        id: 1, 
        text: "What is the capital of France?", 
        options: ["Paris", "London", "Berlin", "Madrid"], 
        correctAnswer: "Paris", 
        image: ParisImage
    },
    { 
        id: 2, 
        text: "What is the largest planet?", 
        options: ["Earth", "Mars", "Jupiter", "Venus"], 
        correctAnswer: "Jupiter", 
        image: PlaneteImage
    },
    // Ajoutez d'autres questions ici
];

const loadQuestionByPosition = (position) => {
    if (position < questions.length) {
        currentQuestion.value = questions[position];
    }
};

const handleAnswerClicked = (selectedAnswer) => {
    console.log("Answer clicked:", selectedAnswer);
    if (selectedAnswer === currentQuestion.value.correctAnswer) {
        score.value++;
    }

    if (currentQuestionPosition.value < questions.length - 1) {
        currentQuestionPosition.value++;
        loadQuestionByPosition(currentQuestionPosition.value);
    } else {
        endQuiz();
    }
};

const endQuiz = () => {
    quizFinished.value = true;
    participationStorageService.saveParticipationScore(score.value);
    console.log("Quiz finished! Your score is:", score.value);
};

onMounted(() => {
    totalNumberOfQuestion.value = questions.length;
    loadQuestionByPosition(currentQuestionPosition.value);
    console.log("Questions Manager mounted");
});
</script>

<template>
    <div v-if="!quizFinished">
        <h1>Bienvenue, {{ playerName }}</h1>
        <br>
        <h2>Question {{ currentQuestionPosition + 1 }} / {{ totalNumberOfQuestion }}</h2>
        <QuestionDisplay :currentQuestion="currentQuestion" @click-on-answer="handleAnswerClicked" />
    </div>
    <div v-else>
        <h1>Quiz Finished!</h1>
        <p>Thank you for participating in the quiz, {{ playerName }}. Your score is: {{ score }} / {{ totalNumberOfQuestion }}</p>
        <h2>Scores des autres joueurs :</h2>
        <div class="scoreboard">
            <div
                v-for="(playerScore, index) in registeredScores"
                :key="playerScore.playerName"
                :class="{
                    first: index === 0,
                    second: index === 1,
                    third: index === 2,
                    other: index >= 3
                }"
            >
                <span class="position">{{ index + 1 }}</span>
                <span class="name">{{ playerScore.playerName }}</span>
                <span class="score">{{ playerScore.score }}</span>
            </div>
        </div>
    </div>
</template>

<style src="../css/Scores.css"></style>
