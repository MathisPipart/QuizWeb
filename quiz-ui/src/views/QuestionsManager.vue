<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import participationStorageService from '@/services/ParticipationStorageService';
import QuestionDisplay from '../views/QuestionDisplay.vue';

const playerName = ref(participationStorageService.getPlayerName() || 'Player');

const currentQuestion = ref({});
const currentQuestionPosition = ref(0);
const totalNumberOfQuestion = ref(0);
const quizFinished = ref(false);
const score = ref(0);

const registeredScores = ref([]);

const questions = ref([]);
const nbQuestions = ref(0);




onMounted(async () => {
    try {
        const response = await api.quiz.get();
        nbQuestions.value = response.data.size;
        console.log("Nb Questions : ", nbQuestions.value);
    } catch (error) {
        console.error("Error fetching quiz data: ", error);
    }

    totalNumberOfQuestion.value = nbQuestions;
    await fetchQuestions();
    
    loadQuestionByPosition(currentQuestionPosition.value);
    registeredScores.value = await fetchRegisteredScores();
    registeredScores.value = getTop5Scores(registeredScores.value);
    console.log("Questions Manager mounted");


});

const fetchQuestions = async () => {
    for (let i = 1; i <= nbQuestions.value; i++) {
        try {
            const response = await api.quiz.question.getByPosition(i);
            const rawQuestion = response.data;

            const formattedQuestion = {
                id: rawQuestion.id,
                text: rawQuestion.title,
                options: rawQuestion.possibleAnswers.map(answer => answer.text),
                correctAnswer: rawQuestion.possibleAnswers.find(answer => answer.isCorrect).text,
                image: rawQuestion.image
            };

            questions.value.push(formattedQuestion);
        } catch (error) {
            console.error("Error fetching question data: ", error);
        }
    }
};

const fetchRegisteredScores = async () => {
    const response = await api.quiz.get();
    return response.data.scores;
};

const getTop5Scores = (scores) => {
    return scores.sort((a, b) => b.score - a.score).slice(0, 5);
};

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
    api.quiz.participation.add({
        playerName: playerName.value,
        score: [1,3,4]
    });
    console.log("Quiz finished! Your score is:", score.value);
};

</script>


<template>
    <div v-if="!quizFinished">
        <h1>Bienvenue, {{ playerName }}</h1>
        <br>
        <h2>Question {{ currentQuestionPosition + 1 }} / {{ totalNumberOfQuestion }}</h2>
        <h2>Score : {{ score }}</h2>
        <div class="question-wrapper">
            <QuestionDisplay :currentQuestion="currentQuestion" @click-on-answer="handleAnswerClicked" />
        </div>
    </div>
    <div v-else>
        <h1>Quiz Finished!</h1>
        <p>Thank you for participating in the quiz, {{ playerName }}. Your score is: {{ score }} / {{ totalNumberOfQuestion }}</p>
        <h2>Meilleurs scores des autres joueurs</h2>
        <div class="scoreboard">
            <div v-for="(playerScore, index) in registeredScores" :key="playerScore.playerName" :class="{
                first: index === 0,
                second: index === 1,
                third: index === 2,
                fourth: index === 3,
                fifth: index === 4,
                other: index >= 5,
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
<style src="../css/Scores.css"></style>