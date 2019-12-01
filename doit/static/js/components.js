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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">All Incidents</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#incidents" onclick="UIkit.accordion(`#dashboard-accordion`).toggle(0);" uk-scroll>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-sun.png" > </div>'
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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">My Incidents</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myincidents-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-sun.png"> </div>'
});

var myopenincidents = new Vue({
	el: '#my-open-incidents',
});

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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">My Backlog</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#mybacklog-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-checklist.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">All Backlog</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#allbacklog-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-checklist.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">My Overdue Cards</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myoverduecards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-beach.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default uk-card-body v-cloak"> <p class="uk-text-center">My Cards</p> <h1 v-if="cards" class="uk-text-warning uk-text-center"> <a class="uk-text-warning" href="#mycards-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-facebook_like.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default uk-card-body v-cloak"> <p class="uk-text-center">My Overdue Boards</p> <h1 v-if="boards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#myoverdueboard-modal" uk-toggle>[[boards]]</a> </h1> <img v-else src="/static/img/icons/icons8-checkmark.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default uk-card-body v-cloak"> <p class="uk-text-center">No Owner or Company</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#noowner-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-ok_hand.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default uk-card-body"> <p class="uk-text-center">Cards I\'m Watching</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#cardswatcher-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-cafe.png"> </div>'
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
	template: '<div class="uk-card-small uk-card-default  uk-card-body v-cloak"> <p class="uk-text-center">Cards Without Due Date</p> <h1 v-if="cards" class="uk-text-danger uk-text-center"> <a class="uk-text-danger" href="#cardswithoutduedate-modal" uk-toggle>[[cards]]</a> </h1> <img v-else src="/static/img/icons/icons8-last_hour_time_and_date.png"> </div>'
});

var cardsnoduedate = new Vue({
	el: '#cards-no-due-date',
});