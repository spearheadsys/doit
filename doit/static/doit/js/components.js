// TODO reuse single component
Vue.component('all-open-incidents-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/allopenincidents/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-inline uk-card-small uk-card-default uk-card-body" style="background-color: lightcoral" v-if="cards"> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Incidents represent a significant impact to productivity."></span> <p class="uk-text-center">All Incidents</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#incidents" onclick="UIkit.accordion(`#dashboard-accordion`).toggle(0);" uk-scroll>[[cards]]</a> </h1> </div>'
});

var allopenincidents = new Vue({
	el: '#all-open-incidents',
});

Vue.component('my-open-incidents-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/myopenincidents/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div v-cloak class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightcoral" v-if="cards"> <p class="uk-text-center">My Incidents</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Incidents represent a significant impact to productivity. These are your highest priority."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#myincidents-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var myopenincidents = new Vue({
	el: '#my-open-incidents',
});

// my-major-cards-component
Vue.component('my-major-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/mymajorcards/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body uk-padding-small" style="background-color: lightsalmon;" v-if="cards"> <p class="uk-text-center">My Major Cards</p> <span uk-icon="question" uk-tooltip="title: Major priority cards, these have business impact and should be prioritized accordingly."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#mymajorcards-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var mymajorcards = new Vue({
	el: '#my-major-cards',
});
// end my-major-cards-component

// mynormalcards
Vue.component('my-normal-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/mynormalcards/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightgoldenrodyellow;" v-if="cards"> <p class="uk-text-center">My Normal Cards</p> <span uk-icon="question" uk-tooltip="title: Normal priority cards, these have limited business impact."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#mynormalcards-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var mynormalcards = new Vue({
	el: '#my-normal-cards',
});
// end mynormalcards

// mylminorcards
Vue.component('my-minor-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/myminorcards/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightgrey;"> <p class="uk-text-center" v-if="cards">My Minor Cards</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#myminorcards-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var myminorcards = new Vue({
	el: '#my-minor-cards',
});
// end myminorcards

Vue.component('my-backlog-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/mybacklog/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="cards"> <p class="uk-text-center">My Backlog</p> <span uk-icon="question" uk-tooltip="title: This is your personal Backlog of cards. The backlog is where you can place new ideas that have not been validated or prioritized/scheduled. Remember to review these at least once a week and prioritise accordingly. If the backlog gets too big, there is something wrong with your workflow and you probably need to spend more time up-front, planning, before engaging."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#mybacklog-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var mybacklog = new Vue({
	el: '#my-backlog-cards',
});

Vue.component('all-backlog-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/allbacklog/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="cards"> <p class="uk-text-center">All Backlog</p> <span uk-icon="question" uk-tooltip="title: These are all cards in the Backlog for this system. Make sure this is reviewed weekly with the entire team and prioritize accordingly. Do not Backlog things just to get them out of the way, you must provide a conscious effort."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#allbacklog-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var mybacklog = new Vue({
	el: '#all-backlog-cards',
});

Vue.component('my-overdue-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/myoverduecards/')
				.then((response) => {
					this.cards = response.data.length;
					this.cardslist = response.data;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightsalmon;" v-if="cards"> <p class="uk-text-center">My Overdue Cards</p> <span uk-icon="question" uk-tooltip="title: These Cards missed their resolution deadline. These should be your highest priority cards unless these are Incidents involving you. You should be working on these before anything else."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span> <a v-else class="uk-text-danger" href="#myoverduecards-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var myoverduecards = new Vue({
	el: '#my-overdue-cards',
});

Vue.component('all-overdue-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/alloverduecards/')
				.then((response) => {
					this.cards = response.data.length;
					this.cardslist = response.data;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="cards"> <p class="uk-text-center">All Overdue Cards</p> <span uk-icon="question" uk-tooltip="title: These are all the Cards in the system. This is here to help you get an overall understanding of team workloads. If you find yourself with free time or happen to know how to help your colleagues advance with one of their Cards, feel free to provide a helping hand."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span> <a v-else class="uk-text-danger" href="#alloverduecards" onclick="UIkit.accordion(\'#dashboard-accordion\').toggle(1); $($.fn.dataTable.tables(true)).DataTable().columns.adjust();" uk-scroll>[[cards]]</a> </h1> </div>'
});

var alloverduecards = new Vue({
	el: '#all-overdue-cards',
});

Vue.component('my-open-cards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/mycards/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="cards"> <p class="uk-text-center">My Cards</p> <span uk-icon="question" uk-tooltip="title: This is a list of your Cards. These are the cards that you alone are directly responsible for without any of the priority filters (Majors, Minor, etc.)."></span> <h1 v-if="cards" class="uk-text-warning uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-warning" href="#mycards-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var myopencards = new Vue({
	el: '#my-open-cards',
});

Vue.component('my-overdue-boards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			boards: []
		}
	},
	mounted: function() {
		this.getBoards();
	},
	methods: {
		getBoards: function() {
			this.loading = true;
			this.$http.get('/api2/myoverdueboards/')
				.then((response) => {
					this.boards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getBoards();
		setInterval(function () {
			this.getBoards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="boards"> <p class="uk-text-center">My Overdue Boards</p> <span uk-icon="question" uk-tooltip="title: These Boards (projects) have missed their deadline."></span> <h1 v-if="boards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#myoverdueboard-modal" uk-toggle>[[boards]]</a> </h1> </div>'
});

var myooverdueboards = new Vue({
	el: '#my-overdue-boards',
});

Vue.component('all-overdue-boards-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			boards: []
		}
	},
	mounted: function() {
		this.getBoards();
	},
	methods: {
		getBoards: function() {
			this.loading = true;
			this.$http.get('/api2/alloverdueboards/')
				.then((response) => {
					this.boards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getBoards();
		setInterval(function () {
			this.getBoards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="boards"> <p class="uk-text-center">All Overdue Boards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These are all the overdue Boards (projects) in the system. This is here to help you get an overall understanding of project status. If you find yourself with free time or happen to know how to help your colleagues advance with one of their projects, feel free to provide a helping hand."></span> <h1 v-if="boards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#alloverdueboard-modal" uk-toggle>[[boards]]</a> </h1> </div>'
});

var alloverdueboards = new Vue({
	el: '#all-overdue-boards',
});

Vue.component('cards-without-owner-or-company-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/noownerorcompany/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body uk-background-secondary" v-if="cards" v-cloak> <p class="uk-text-center">No Owner or Company</p> <span uk-icon="question" uk-tooltip="title: These cards are not assigned! Make sure there is an owner an associated company."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center" > <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#noowner-modal" uk-toggle> [[cards]] </a></h1></div>'
});

var noownerorcompany = new Vue({
	el: '#no-owner-or-company',
});

Vue.component('cards-im-watching',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/cardswatcher/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-inline uk-card-default uk-card-body" v-if="cards"> <p class="uk-text-center">Cards I\'m Watching</p> <span uk-icon="question" uk-tooltip="title: Watchers are not expected to resolve Cards however you may be there to offer some help or to learn.;"></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><span v-else><a class="uk-text-danger" href="#cardswatcher-modal" uk-toggle>[[cards]]</a></span> </h1> </div>'
});

var cardswatcher = new Vue({
	el: '#cards-watcher',
});

// cards no due date
Vue.component('cards-no-due-date-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.getCards();
	},
	methods: {
		getCards: function() {
			this.loading = true;
			this.$http.get('/api2/cardswoduedate/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" v-if="cards"> <p class="uk-text-center">Cards Without Due Date</p> <span uk-icon="question" uk-tooltip="title: These Cards are missing a due date. Every card in the system should have a due date.; pos: bottom-left;"></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#cardswithoutduedate-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var cardsnoduedate = new Vue({
	el: '#cards-no-due-date',
});

// cards sla breached component
Vue.component('card-sla-breached-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			isBreached: []
		}
	},
	mounted: function() {
		this.isBreached();
	},
	methods: {
		isBreached: function() {
			this.loading = true;
			this.$http.get('/cards/cardsla/${[[id]]}/')
				.then((response) => {
					this.cardsla = response.data;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.isBreached();

		setInterval(function () {
			this.isBreached();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightsalmon;"> <p class="uk-text-center">My Major Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Major priority cards, these have business impact."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#all-cards-sla-breached-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

// cards ALL sla breached component
Vue.component('all-cards-sla-breached-component',{
	delimiters: ['[[', ']]'],
	props: '',
	data: function () {
		return {
			cards: []
		}
	},
	mounted: function() {
		this.isBreached();
	},
	methods: {
		isBreached: function() {
			this.loading = true;
			this.$http.get('/api2/allslabreached/')
				.then((response) => {
					this.cards = response.data.length;
					this.loading = false;
				})
				.catch((err) => {
				 this.loading = false;
				 console.log(err);
				})
		},
	},
	created: function () {
		this.isBreached();

		setInterval(function () {
			this.isBreached();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body" style="background-color: lightsalmon;"> <p class="uk-text-center" v-if="cards">Outside of SLA</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Cards outside of SLA."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <span v-if="loading" uk-spinner></span><a v-else class="uk-text-danger" href="#all-cards-sla-breached-modal" uk-toggle>[[cards]]</a> </h1> </div>'
});

var cardSlaBreached = new Vue({
	el: '#all-cards-sla-breached',
});

