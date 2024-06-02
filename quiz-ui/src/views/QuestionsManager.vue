<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
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

const registeredScores = ref([]);

const questions = ref([]);
// const questions = [
//     {
//         id: 1,
//         text: "What is the capital of France?",
//         options: ["Paris", "London", "Berlin", "Madrid"],
//         correctAnswer: "Paris",
//         image: ParisImage
//     },
//     {
//         id: 2,
//         text: "What is the largest planet?",
//         options: ["Earth", "Mars", "Jupiter", "Venus"],
//         correctAnswer: "Jupiter",
//         image: PlaneteImage
//     },
//     // Ajoutez d'autres questions ici
// ];

onMounted(async () => {
    console.log((await api.quiz.question.getByPosition(1)).data);
    console.log((await api.quiz.question.getByPosition(2)).data);
    console.log((await api.quiz.question.getByPosition(3)).data);
    const response = await api.quiz.question.getByPosition(1);
    const rawQuestion = response.data;

    const formattedQuestion = {
        id: rawQuestion.id,
        text: rawQuestion.title,
        options: rawQuestion.possibleAnswers.map(answer => answer.text),
        correctAnswer: rawQuestion.possibleAnswers.find(answer => answer.isCorrect).text,
        image: rawQuestion.image
    };

    questions.value.push(formattedQuestion); // Ajoute la question formatée au tableau des questions

    console.log(formattedQuestion.id);
    console.log(formattedQuestion.text);
    console.log(formattedQuestion.options);


    registeredScores.value = await (await api.quiz.get()).data.scores;

    totalNumberOfQuestion.value = questions.value.length;
    loadQuestionByPosition(currentQuestionPosition.value);
    console.log("Questions Manager mounted");
});

const loadQuestionByPosition = (position) => {
    if (position < questions.value.length) {
        currentQuestion.value = questions.value[position];
    }
};

const handleAnswerClicked = (selectedAnswer) => {
    console.log("Answer clicked:", selectedAnswer);
    if (selectedAnswer === currentQuestion.value.correctAnswer) {
        score.value++;
    }

    if (currentQuestionPosition.value < questions.value.length - 1) {
        setTimeout(() => {
            currentQuestionPosition.value++;
            loadQuestionByPosition(currentQuestionPosition.value);
        }, 1000); // Attendre 1 seconde avant de passer à la question suivante
    } else {
        setTimeout(() => {
            endQuiz();
        }, 1000); // Attendre 1 seconde avant de terminer le quiz
    }
};

const endQuiz = () => {
    quizFinished.value = true;
    participationStorageService.saveParticipationScore(score.value);
    console.log("Quiz finished! Your score is:", score.value);
};
</script>

<template>
    <div v-if="!quizFinished">
        <h1>Bienvenue, {{ playerName }}</h1>
        <br>
        <h2>Question {{ currentQuestionPosition + 1 }} / {{ totalNumberOfQuestion }}</h2>
        <div class="question-wrapper">
            <QuestionDisplay :currentQuestion="currentQuestion" @click-on-answer="handleAnswerClicked" />
        </div>
    </div>
    <div v-else>
        <h1>Quiz Finished!</h1>
        <p>Thank you for participating in the quiz, {{ playerName }}. Your score is: {{ score }} / {{
            totalNumberOfQuestion }}</p>
        <h2>Meilleurs scores des autres joueurs</h2>
        <div class="scoreboard">
            <div v-for="(playerScore, index) in registeredScores" :key="playerScore.playerName" :class="{
                first: index === 0,
                second: index === 1,
                third: index === 2,
                other: index >= 3
            }">
                <span class="position">{{ index + 1 }}</span>
                <span class="name">{{ playerScore.playerName }}</span>
                <span class="score">{{ playerScore.score }}</span>
            </div>
        </div>
        <!-- Bouton pour revenir à la page Home -->
        <RouterLink to="/" class="home-button">
            Revenir à la page Home
        </RouterLink>
    </div>
</template>

<style scoped>
.question-wrapper {
    width: 100%;
    max-width: 800px;
    margin-top: 2rem;
}

.home-button {
    display: inline-block;
    margin-top: 2rem;
    padding: 0.5rem 1rem;
    background-color: #41b883;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-weight: bold;
    text-align: center;
}

.home-button:hover {
    background-color: #3a9d70;
}
</style>
