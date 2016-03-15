var Game = {
    // 这里是轮询请求的地址
    url: 'http://121.52.235.231:40013/page_v3/game',
    rest: $('.rest'),
    nameA: $('.name-a'),
    nameB: $('.name-b'),
    handA: $('.hand-a'),
    handB: $('.hand-b'),
    tableA: $('.table-a'),
    tableB: $('.table-b'),
    regionImg: $('.region-img'),
    cover: $('.cover'),
    popupPlayer: $('.popup-player'),
    player: [],
    colorList: { A: '#9e21ff', B: '#006cff', C: '#1eb600', D: '#ff9600', E: '#ff4343', F: '#ffd200' },

    init: function() {
        var self = this;
        setTimeout(function() {
            self.request();
        }, 1000);
    },

    request: function() {
        var self = Game;
        $.ajax({
            type: 'get',
            url: self.url,
            timeout: 5 * 1000,
            dataType: 'json',
            success: function(ret) {
                // console.log(ret);
                // 默认返回的结果就是一条command格式的json数据
                ret && self.handleCmd(ret);
                setTimeout(function() {
                    self.request();
                }, 1000);
            },
            error: function() {
                console.log('txm ajax error!');
                setTimeout(function() {
                    self.request();
                }, 1000);
            }
        });
    },

    handleCmd: function(cmd) {
        var self = this;
        switch (cmd.command) {
            case 'game_start':
                self.startGame(cmd);
                break;
            case 'get_card':
                self.getCard(cmd);
                break;
            case 'action':
                self.action(cmd);
                break;
            case 'region_win':
                self.regionWin(cmd);
                break;
            case 'game_win':
                self.gameWin(cmd);
                break;
        }
    },

    startGame: function(cmd) {
        var self = this;
        self.rest.html(60);
        self.nameA.html(cmd['player0']);
        self.nameB.html(cmd['player1']);
        self.player.push(cmd['player0']);
        self.player.push(cmd['player1']);
    },

    getCard: function(cmd) {
        var self = this;
        var color = self.colorList[cmd['card'].slice(0, 1)];
        var num = cmd['card'].slice(1);
        var handle = cmd['player'] == '0' ? self.handA : self.handB;
        var first = $(handle.find('div[data-num=""]')[0]);
        first.html(num).attr('data-num', cmd['card']).css({
            'background-color': color,
            '-webkit-animation': 'blink 1s 1'
        });
        self.rest.html(self.rest.html()-1);
        setTimeout(function() {
            first.css('-webkit-animation', '');
        }, 1000);
    },

    action: function(cmd) {
        var self = this;
        var color = self.colorList[cmd['card'].slice(0, 1)];
        var num = cmd['card'].slice(1);
        var handle = cmd['player'] == '0' ? self.handA : self.handB;
        var table = cmd['player'] == '0' ? self.tableA : self.tableB;
        var selected = handle.find('div[data-num="' + cmd['card'] + '"]');
        var region = $(table.find('.region' + cmd['region'] + '[data-num=""]')[0]);
        var node = $('<div>' + num + '</div>');
        node.css('background-color', color);
        selected.html('').css('background-color', '#d6d6d6').attr('data-num', '');
        region.attr('data-num', cmd['card']).append(node);
    },

    regionWin: function(cmd) {
        var self = this;
        var img = $(self.regionImg[cmd['region']]);
        var src = cmd['player'] == '0' ? 'image/orange.png' : 'image/blue.png';
        img.attr('src', src).css({
            '-webkit-animation': 'blink2 1s 1'
        });;
    },

    gameWin: function(cmd) {
        var self = this;
        self.popupPlayer.html('玩家 ' + self.player[cmd['player']]);
        self.cover.removeClass('display-none');
    }
}

// 正常运行只要调用以下代码即可，就会开始不断轮询
//Game.init();


// 以下是演示代码
// 增加了一个可选自断interval，来控制下一步的时间间隔，当没有时默认为1000毫秒，也就是1秒
var CmdList = [
{ 'command': 'game_start', 'player0': '啦啦啦', 'player1': '德玛西亚' },
{'player': '0', 'command': 'get_card', 'card': 'D6'},
{'player': '0', 'command': 'get_card', 'card': 'C6'},
{'player': '0', 'command': 'get_card', 'card': 'B3'},
{'player': '0', 'command': 'get_card', 'card': 'D2'},
{'player': '0', 'command': 'get_card', 'card': 'C5'},
{'player': '0', 'command': 'get_card', 'card': 'F7'},
{'player': '0', 'command': 'get_card', 'card': 'F4'},
{'player': '0', 'region': 5, 'command': 'action', 'card': 'C6'},
{'player': '1', 'command': 'get_card', 'card': 'B9'},
{'player': '1', 'command': 'get_card', 'card': 'B1'},
{'player': '1', 'command': 'get_card', 'card': 'D1'},
{'player': '1', 'command': 'get_card', 'card': 'C8'},
{'player': '1', 'command': 'get_card', 'card': 'A2'},
{'player': '1', 'command': 'get_card', 'card': 'B2'},
{'player': '1', 'command': 'get_card', 'card': 'F9'},
{'player': '1', 'region': 5, 'command': 'action', 'card': 'B9'},
{'player': '0', 'command': 'get_card', 'card': 'A9'},
{'player': '0', 'region': 5, 'command': 'action', 'card': 'C5'},
{'player': '1', 'command': 'get_card', 'card': 'F8'},
{'player': '1', 'region': 6, 'command': 'action', 'card': 'F9'},
{'player': '0', 'command': 'get_card', 'card': 'F2'},
{'player': '0', 'region': 6, 'command': 'action', 'card': 'F7'},
{'player': '1', 'command': 'get_card', 'card': 'B6'},
{'player': '1', 'region': 6, 'command': 'action', 'card': 'F8'},
{'player': '0', 'command': 'get_card', 'card': 'A3'},
{'player': '0', 'region': 7, 'command': 'action', 'card': 'A9'},
{'player': '1', 'command': 'get_card', 'card': 'D9'},
{'player': '1', 'region': 7, 'command': 'action', 'card': 'B6'},
{'player': '0', 'command': 'get_card', 'card': 'F3'},
{'player': '0', 'region': 8, 'command': 'action', 'card': 'F4'},
{'player': '1', 'command': 'get_card', 'card': 'A8'},
{'player': '1', 'region': 8, 'command': 'action', 'card': 'A8'},
{'player': '0', 'command': 'get_card', 'card': 'E4'},
{'player': '0', 'region': 8, 'command': 'action', 'card': 'F3'},
{'player': '1', 'command': 'get_card', 'card': 'C3'},
{'player': '1', 'region': 0, 'command': 'action', 'card': 'D9'},
{'player': '0', 'command': 'get_card', 'card': 'A10'},
{'player': '0', 'region': 7, 'command': 'action', 'card': 'A10'},
{'player': '1', 'command': 'get_card', 'card': 'A6'},
{'player': '1', 'region': 8, 'command': 'action', 'card': 'A6'},
{'player': '0', 'command': 'get_card', 'card': 'D3'},
{'player': '0', 'region': 0, 'command': 'action', 'card': 'B3'},
{'player': '1', 'command': 'get_card', 'card': 'E2'},
{'player': '1', 'region': 1, 'command': 'action', 'card': 'A2'},
{'player': '0', 'command': 'get_card', 'card': 'C2'},
{'player': '0', 'region': 0, 'command': 'action', 'card': 'A3'},
{'player': '1', 'command': 'get_card', 'card': 'E6'},
{'player': '1', 'region': 1, 'command': 'action', 'card': 'B2'},
{'player': '0', 'command': 'get_card', 'card': 'C4'},
{'player': '0', 'region': 1, 'command': 'action', 'card': 'D2'},
{'player': '1', 'command': 'get_card', 'card': 'C7'},
{'player': '1', 'region': 2, 'command': 'action', 'card': 'C8'},
{'player': '0', 'command': 'get_card', 'card': 'A1'},
{'player': '0', 'region': 1, 'command': 'action', 'card': 'F2'},
{'player': '1', 'command': 'get_card', 'card': 'B5'},
{'player': '1', 'region': 2, 'command': 'action', 'card': 'C7'},
{'player': '0', 'command': 'get_card', 'card': 'E9'},
{'player': '0', 'region': 2, 'command': 'action', 'card': 'E9'},
{'player': '1', 'command': 'get_card', 'card': 'D4'},
{'player': '1', 'region': 7, 'command': 'action', 'card': 'B5'},
{'player': '0', 'command': 'get_card', 'card': 'A5'},
{'player': '0', 'region': 3, 'command': 'action', 'card': 'D6'},
{'player': '1', 'command': 'get_card', 'card': 'F6'},
{'player': '1', 'region': 3, 'command': 'action', 'card': 'E6'},
{'player': '0', 'command': 'get_card', 'card': 'A7'},
{'player': '0', 'region': 4, 'command': 'action', 'card': 'A7'},
{'player': '1', 'command': 'get_card', 'card': 'F10'},
{'player': '1', 'region': 6, 'command': 'action', 'card': 'F10'},
{'player': '0', 'command': 'get_card', 'card': 'C10'},
{'player': '0', 'region': 4, 'command': 'action', 'card': 'A5'},
{'player': '1', 'command': 'get_card', 'card': 'E10'},
{'player': '1', 'region': 4, 'command': 'action', 'card': 'E10'},
{'player': '0', 'command': 'get_card', 'card': 'E8'},
{'player': '0', 'region': 2, 'command': 'action', 'card': 'E8'},
{'player': '1', 'command': 'get_card', 'card': 'A4'},
{'player': '1', 'region': 0, 'command': 'action', 'card': 'F6'},
{'player': '0', 'command': 'get_card', 'card': 'C9'},
{'player': '0', 'region': 0, 'command': 'action', 'card': 'D3'},
{'player': '1', 'command': 'get_card', 'card': 'F1'},
{'player': '1', 'region': 3, 'command': 'action', 'card': 'D4'},
{'player': '0', 'command': 'get_card', 'card': 'D8'},
{'player': '0', 'region': 2, 'command': 'action', 'card': 'E4'},
{'player': '1', 'command': 'get_card', 'card': 'F5'},
{'player': '1', 'region': 8, 'command': 'action', 'card': 'A4'},
{'player': '0', 'command': 'get_card', 'card': 'E1'},
{'player': '0', 'region': 3, 'command': 'action', 'card': 'D8'},
{'player': '1', 'command': 'get_card', 'card': 'B10'},
{'player': '1', 'region': 5, 'command': 'action', 'card': 'B10'},
{'player': '0', 'command': 'get_card', 'card': 'D5'},
{'player': '0', 'region': 3, 'command': 'action', 'card': 'D5'},
{'player': '1', 'command': 'get_card', 'card': 'E5'},
{'player': '1', 'region': 4, 'command': 'action', 'card': 'F5'},
{'player': '0', 'command': 'get_card', 'card': 'B7'},
{'player': '0', 'region': 4, 'command': 'action', 'card': 'A1'},
{'player': '1', 'command': 'get_card', 'card': 'E7'},
{'player': '1', 'region': 7, 'command': 'action', 'card': 'B1'},
{'player': '0', 'command': 'get_card', 'card': 'B4'},
{'player': '0', 'region': 6, 'command': 'action', 'card': 'B7'},
{'player': '1', 'command': 'get_card', 'card': 'D10'},
{'player': '1', 'region': 1, 'command': 'action', 'card': 'E2'},
{'player': '0', 'command': 'get_card', 'card': 'D7'},
{'player': '0', 'region': 5, 'command': 'action', 'card': 'C4'},
{'player': '1', 'command': 'get_card', 'card': 'C1'},
{'player': '1', 'region': 2, 'command': 'action', 'card': 'C1'},
{'player': 0, 'region': '2', 'command': 'region_win'},
{'player': '0', 'command': 'get_card', 'card': 'B8'},
{'player': '0', 'region': 6, 'command': 'action', 'card': 'D7'},
{'player': 1, 'region': '6', 'command': 'region_win'},
{'player': '1', 'command': 'get_card', 'card': 'E3'},
{'player': '1', 'region': 3, 'command': 'action', 'card': 'E5'},
{'player': 0, 'region': '3', 'command': 'region_win'},
{'player': '0', 'region': 1, 'command': 'action', 'card': 'C2'},
{'player': 1, 'region': '1', 'command': 'region_win'},
{'player': '1', 'region': 5, 'command': 'action', 'card': 'E3'},
{'player': 0, 'region': '5', 'command': 'region_win'},
{'player': '0', 'region': 7, 'command': 'action', 'card': 'B8'},
{'player': 1, 'region': '7', 'command': 'region_win'},
{'player': '1', 'region': 0, 'command': 'action', 'card': 'D10'},
{'player': 0, 'region': '0', 'command': 'region_win'},
{'player': '0', 'region': 8, 'command': 'action', 'card': 'B4'},
{'player': 1, 'region': '8', 'command': 'region_win'},
{'player': '1', 'command': 'game_win'},
];

(function execute() {
    var cmd = CmdList.shift();
    if (cmd) {
        Game.handleCmd(cmd);
        setTimeout(execute, cmd['interval'] || 1000);
    } 
})();
