import { createRouter, createWebHistory } from 'vue-router';
import IndexIndex from '@/views/IndexIndex.vue';
import AdminLogin from '@/views/admin_views/AdminLogin.vue';
import AdminDashboard from '@/views/admin_views/AdminDashboard.vue';
import CreateChapter from '@/views/admin_views/CreateChapter.vue';
import CreateSubject from '@/views/admin_views/CreateSubject.vue';
import QuizManagement from '@/views/admin_views/QuizManagement.vue';
import AddQuestion from '@/views/admin_views/AddQuestion.vue';
import AddQuiz from '@/views/admin_views/AddQuiz.vue';
import UserLogin from '@/views/user_views/UserLogin.vue';
import UserDashboard from '@/views/user_views/UserDashboard.vue';
import TakeQuiz from '@/views/user_views/TakeQuiz.vue';
import ManageChapterQuizzes from '@/views/admin_views/ManageChapterQuizzes.vue';
import UserRegister from '@/views/user_views/UserRegister.vue';
import UserAttempts from '@/views/user_views/UserAttempts.vue';
import UserSummary from '@/views/user_views/UserSummary.vue';
import AdminSummary from '@/views/admin_views/AdminSummary.vue';
import SearchResults from '@/views/admin_views/SearchResults.vue';
import Userprofile from '@/views/user_views/Userprofile.vue';
import AdminExport from '@/views/admin_views/AdminExport.vue';
import UserSearchResults from '@/views/user_views/UserSearchResults.vue';
import AiAgent from '@/views/user_views/AiAgent.vue';
import UserLeaderboard from '@/views/user_views/UserLeaderboard.vue';

const routes = [
  { path: '/', name: 'Home', component: IndexIndex },
  { path: '/admin_login', name: 'AdminLogin', component: AdminLogin },
  { path: '/user_login', name: 'UserLogin', component: UserLogin },
  { path: '/admin_dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/create_subject', name: 'CreateSubject', component: CreateSubject },
  { path: '/create_chapter/:subjectId', name: 'CreateChapter', component: CreateChapter },
  { path: '/quiz_management', name: 'QuizManagement', component: QuizManagement },
  { path: '/add_question', name: 'AddQuestion', component: AddQuestion },
  { path: '/add_quiz', name: 'AddQuiz', component: AddQuiz },
  { path: '/user_login', name: 'UserLogin', component: UserLogin },
  { path: '/user_dashboard', name: 'UserDashboard', component: UserDashboard },
  { path: '/take_quiz/:quizId', name: 'TakeQuiz', component: TakeQuiz },
  { path: '/manage_chapter_quizzes/:chapterId', name: 'ManageChapterQuizzes', component: ManageChapterQuizzes, props: true },
  { path: '/user_register', name: 'UserRegister', component: UserRegister },
  { path: '/user_attempts', name: 'UserAttempts', component: UserAttempts },
  { path: '/user_summary', name: "UserSummary", component: UserSummary },
  { path: "/admin_summary", name: "AdminSummary", component: AdminSummary },
  { path: "/admin_search/:query", name: "SearchResults", component: SearchResults },
  { path: "/get_user_profile_details", name: "UserProfile", component: Userprofile },
  { path: '/admin_export', name: "AdminExport", component: AdminExport },
  { path: '/user_search/:query', name: "UserSearchResults", component: UserSearchResults },
  { path: '/generate_ai_content', name: "AiAgent", component: AiAgent },
  { path: '/user_leaderboard', name: 'UserLeaderboard', component: UserLeaderboard },












];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
