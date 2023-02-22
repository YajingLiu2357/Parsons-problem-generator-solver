import { createStore } from 'vuex'
import VuexPersistence from 'vuex-persist'

const vuexLocalStorage = new VuexPersistence({
    key: 'vuex',
    storage: window.localStorage,
})

export default createStore({
    state:{
        hello:'Vue-SPA-Quickstart',
        userStatus: 'visitor',  // visitor, student, teacher, admin
        activeTab: '',
        userEmail: '',
        userName: '',
        UID: '',
    },
    mutations: {
        setUser(state, payload){
            state.UID = payload.UID;
            state.userEmail = payload.userEmail;
            state.userName = payload.userName;
            state.userStatus = payload.userStatus;
        },
        chgUser(state, payload){
            state.UID = payload.UID;
            state.userEmail = payload.userEmail;
            state.userName = payload.userName;
        },
        chgStatus(state, payload){
            state.userStatus = payload.userStatus;
        },
        signOut(state){
            state.UID = '';
            state.userEmail = '';
            state.userName = '';
            state.activeTab = '';
            state.userStatus = 'visitor';
        },
    },
    actions: {},
    plugins: [vuexLocalStorage.plugin]
})