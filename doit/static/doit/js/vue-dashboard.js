// make sure we send csrf django token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

Vue.http.headers.common['X-CSRF-TOKEN'] = csrftoken;
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken;

// my_incidents
var my_incidents = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my-incidents',
	data: {
		my_incidents: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/myopenincidents', function (response) {
				this.my_incidents = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/myopenincidents/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})

// my_majorcards
var my_majorcards = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my-majorcards',
	data: {
		my_majorcards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/mymajorcards', function (response) {
				this.my_majorcards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/mymajorcards/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})
//end my_majorcards

// my_normalcards
var my_normalcards = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my-normalcards',
	data: {
		my_normalcards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/mynormalcards', function (response) {
				this.my_normalcards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/mynormalcards/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})
// end my_normalcards


// all-cards-sla-breached-table
var all_cards_sla_breached = new Vue({
	delimiters: ['[[', ']]'],
	el: '#all-cards-sla-breached-table',
	data: {
		cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/allslabreached/', function (response) {
				this.cards = response;
			}.bind(this));
		},
		// todo: i belive that because of caching this does not work
		// we can just call deletecard/cardid
		// deleteCard: function(id) {
		// 	this.loading = true;
		// 	if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
		// 		this.$http.delete(`/api2/allslabreached/${[[id]]}/`)
		// 			.then((response) => {
		// 				this.loading = false;
		// 				this.loadData();
		// 			})
		// 			.catch((err) => {
		// 				this.loading = false;
		// 				console.log(err);
		// 			})
		// 	}
		// },
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})
// end all-cards-sla-breached-table

// my_normalcards
var my_minorcards = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my-minorcards',
	data: {
		my_minorcards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/myminorcards', function (response) {
				this.my_minorcards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/myminorcards/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})
// end my_minorcards

//all_my_open_cards
var all_my_open_cards = new Vue({
	delimiters: ['[[', ']]'],
	el: '#all_my_open_cards',
	data: {
		all_my_open_cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/cards/all_my_open_cards', function (response) {
				this.all_my_open_cards = response.allmycards;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/mycards/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})

//my_backlogs
var my_backlog = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my-backlog',
	data: {
		cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/mybacklog/', function (response) {
				this.cards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			this.$http.delete(`/api2/mybacklog/${[[id]]}/`)
				.then((response) => {
					this.loading = false;
					this.loadData();
				})
				.catch((err) => {
					this.loading = false;
					console.log(err);
				})
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})

//all_backlogs
var all_backlog = new Vue({
	delimiters: ['[[', ']]'],
	el: '#all-backlog',
	data: {
		cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/allbacklog/', function (response) {
				this.cards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/allbacklog/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})

// my_overdue_cards_list
var my_overdue_cards_list = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_overdue_cards_list',
	data: {
		my_overdue_cards_list: '',
		loading: false,
		currentCard: {},
	},
	methods: {
		loadData: function () {
			$.get('/cards/my_overdue_cards_list', function (response) {
				this.my_overdue_cards_list = response.my_overdue_cards_list;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/mycards/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
  		}
		}
})

// my_overdue_board_list
var my_overdue_boards_list = new Vue({
	delimiters: ['[[', ']]'],
	el: '#my_overdue_boards_list',
	data: {
		my_overdue_boards_list: '',
		loading: false,
		currentCard: {},
	},
	methods: {
		loadData: function () {
			$.get('/api2/myoverdueboards/', function (response) {
				this.my_overdue_boards_list = response;
			}.bind(this));
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
  		}
		}
})

// all_overdue_board_list
var all_overdue_boards_list = new Vue({
	delimiters: ['[[', ']]'],
	el: '#all_overdue_boards_list',
	data: {
		all_overdue_boards_list: '',
		loading: false,
		currentCard: {},
	},
	methods: {
		loadData: function () {
			$.get('/api2/alloverdueboards/', function (response) {
				this.all_overdue_boards_list = response;
			}.bind(this));
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  	moment: function (date) {
    	return moment(date).format('MMM Do YYYY, k:m');
  		}
		}
})



// cards without owner
var cards_without_owner_or_company = new Vue({
	delimiters: ['[[', ']]'],
	el: '#cards_without_owner',
	data: function () {
		return {
			no_owner_or_company: []
		}
	},
	methods: {
		loadData: function () {
			$.get('/api2/noownerorcompany', function (response) {
				this.no_owner_or_company = response;
				// console.log(response.data);
			}.bind(this));
		},
	deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/noownerorcompany/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
	moment: function (date) {
		return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})


// cards im watching
var cards_watcher = new Vue({
	delimiters: ['[[', ']]'],
	el: '#cards_watcher',
	data: function () {
		return {
			cards: []
		}
	},
	methods: {
		loadData: function () {
			$.get('/api2/cardswatcher', function (response) {
				this.cards = response;
				// console.log(response.data);
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/cardswatcher/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    	return moment();
  	}
	},
	created: function () {
		this.loadData();
		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
	moment: function (date) {
		return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})


// cards no due date
//my_backlogs
var no_duedate = new Vue({
	delimiters: ['[[', ']]'],
	el: '#cards-without-due-date',
	data: {
		cards: ''
	},
	methods: {
		loadData: function () {
			$.get('/api2/cardswoduedate/', function (response) {
				this.cards = response;
			}.bind(this));
		},
		deleteCard: function(id) {
			this.loading = true;
			if(confirm("This is a non-recoverable operation! All related items (tasks, attachments, etc.) will also be removed! Are you sure?")) {
				this.$http.delete(`/api2/cardswoduedate/${[[id]]}/`)
					.then((response) => {
						this.loading = false;
						this.loadData();
					})
					.catch((err) => {
						this.loading = false;
						console.log(err);
					})
			}
		},
		moment: function () {
    		return moment();
  	}
	},
	created: function () {
		this.loadData();

		setInterval(function () {
			this.loadData();
		}.bind(this), 90000);
	},
	beforeDestroy: function(){
		clearInterval(this.interval);
	},
	filters: {
  		moment: function (date) {
			return moment(date).format('MMM Do YYYY, k:m');
		}
	}
})



