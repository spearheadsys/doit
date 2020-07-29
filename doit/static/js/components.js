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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-inline uk-card-small uk-card-default  uk-card-body v-cloak" style="background-color: lightcoral"> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Incidents represent a significant impact to productivity."></span> <p class="uk-text-center">All Incidents</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#incidents" onclick="UIkit.accordion(`#dashboard-accordion`).toggle(0);" uk-scroll>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg" > </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak" style="background-color: lightcoral"> <p class="uk-text-center">My Incidents</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Incidents represent a significant impact to productivity. These are your highest priority."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myincidents-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak" style="background-color: lightsalmon;"> <p class="uk-text-center">My Major Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Major priority cards, these have business impact."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#mymajorcards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak" style="background-color: lightgoldenrodyellow;"> <p class="uk-text-center">My Normal Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Normal priority cards, these have limited business impact."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#mynormalcards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak" style="background-color: lightgrey;"> <p class="uk-text-center">My Minor Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: Minor priority cards."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myminorcards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">My Backlog</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: This is your personal Backlog of cards. The backlog is where you can place new ideas that have not been validated or prioritized/scheduled. Remember to review these at least once a week and prioritise accordingly. If the backlog gets too big, there is something wrong with you workflow and you probably need to spend more time up-front, planning, before engaging."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#mybacklog-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">All Backlog</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These are all cards in the Backlog for this system. Make sure this is reviewed weekly by the entire team and proritized accordinlgy otherwsie this will get out of hand quickly: too much planning and not enough action or too much action and not enough planning means we want to do things, but not planning accordingly or doing things but not planning enough. Do not Backlog things just to get them out of the way, you must provide a concious effort in planning otherwise things will not get done by ignoring them."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#allbacklog-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">My Overdue Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These are your Overdue cards meaning you missed their deadline. These should be your highest priority cards unless these are Incidents involving you. You should be working on these before anything else avoid extending this overdue period at all costs. If you need help, get some colleagues involved or ask you manager to help. Anytime a card overruns its duedate our customers can give us a negative rating. The performance of this metric is paramount to the overall performance of our team, make sure you update deadlines accordingly and avoid missing these deadline by getting things done right and on time. If you know you are going to miss a deadline, you must announce you manager and update the deadline."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myoverduecards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
});

var myoverduecards = new Vue({
	el: '#my-overdue-cards',
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">My Cards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: This is a list of your Cards. These are the cards that you alone are directly responsible for. Work on these if you do not have Incidents or Overdue cards but always prioritise by severty and due date: do whatever it takes to avoid missing deadlines and always make sure you are working on the right thing at the right time (service type, priority, due date)."></span> <h1 v-if="cards" class="uk-text-warning uk-text-center"> <a class="uk-text-warning" href="#mycards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">My Overdue Boards</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These are your Overdue boards (projects). Make sure you are not missing deadlines on your projects by reviewieng them at least once a week. The review is not enough however, you also need to get things done. Keep projects on-track and on-time by reviewing, delegating where possible and asking for help if things are not progressing. Avoid delivering bad news when the deadline occurs: your review should catch and announce any potential missed deadlines long before they happen so that we can extend these and communicate to our customers and partners in a timely manner."></span> <h1 v-if="boards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myoverdueboard-modal" uk-toggle>[[boards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
});

var myooverdueboards = new Vue({
	el: '#my-overdue-boards',
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak uk-background-secondary"> <p class="uk-text-center">No Owner or Company</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These cards may go unnoticed. Make sure there is an owner an ssociated company."></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#noowner-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-inline uk-card-default uk-card-body v-cloak"> <p class="uk-text-center">Cards I\'m Watching</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These are Cards you are watching. Watching means just that, you are not expected to resolve them, that is the Owners job, however you may be there to offer some help or other input or possibly to learn. Make sure you understand why you are a watcher and if you have no value, remove yourself from these cards as they will just generate noise. If you are there for a reason however, treat these as if they were your own and ask the Owner where you can help. Do whatever you can to make sure we do not miss deadlines and keep things moving.; pos: bottom-left;"></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#cardswatcher-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
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
				 //console.log(err);
				})
		},
	},
	created: function () {
		this.getCards();

		setInterval(function () {
			this.getCards();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	template: '<div class="uk-card-small uk-card-default uk-inline uk-card-body v-cloak"> <p class="uk-text-center">Cards Without Due Date</p> <span class="uk-margin-small-right uk-margin-small-bottom uk-position-bottom-right" uk-icon="question" uk-tooltip="title: These Cards are missing a due date. Every card in the system should have a due date. Make sure you assign a due date to all cards that you take over or are watching. Do not just put an unrealistic due date, it is better to leave no due date than to exaggerate and try to put a very long one however note that cards without due dates are considered bad practice and are negatively accounted for in our scoreboards.Ω; pos: bottom-left;"></span> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#cardswithoutduedate-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/sph-zero.svg"> </div>'
});

var cardsnoduedate = new Vue({
	el: '#cards-no-due-date',
});