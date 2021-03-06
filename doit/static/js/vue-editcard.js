// open tasks
var open_tasks = new Vue({
	delimiters: ['[[', ']]'],
	el: '#opentasks',
	data: {
		open_tasks: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/gettaskcount?card=' + cardid, function (response) {
				this.open_tasks = response;
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

// open tasks
var example1 = new Vue({
	delimiters: ['[[', ']]'],
	el: '#example-1',
	data: {
		open_tasks: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/gettasks?card=' + cardid, function (response) {
				this.open_tasks = response;
				if(this.open_tasks.done){
						var checked = "checked";
				} else {
						checked = '';
				}
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();
	},
})


// reminders
var reminders = new Vue({
	delimiters: ['[[', ']]'],
	el: '#vue_reminders',
	data: {
		open_reminders: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/getreminderscount?card=' + cardid, function (response) {
				this.open_reminders = response;
			}.bind(this));
		}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 60000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	}
})
