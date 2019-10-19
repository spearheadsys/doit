
// my_cards
var my_open = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_vue_cards',
	data: {
		my_open_cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/my_vue_cards', function (response) {
				this.my_open_cards = response.open_cards;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})

// my_overdue_cards
var my_overdue = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_vue_overdue',
	data: {
		my_overdue_cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/my_vue_overdue', function (response) {
				this.my_overdue_cards = response.overdue_cards;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})

// cards without owner
var cards_without_owner = new Vue({
	delimiters: ['[[', ']]'],
	el: '#cards_without_owner',
	data: {
		cards_without_owner: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/cards_without_owner', function (response) {
				this.cards_without_owner = response.cards_without_owner;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})


//  cards_without_company
var cards_without_company = new Vue({
	delimiters: ['[[', ']]'],
	el: '#cards_without_company',
	data: {
		cards_without_company: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/cards_without_company', function (response) {
				this.cards_without_company = response.cards_without_company;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 20000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})