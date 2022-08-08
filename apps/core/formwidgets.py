# -*- coding: utf-8 -*-
from django.forms.widgets import HiddenInput, SelectMultiple, RadioSelect, CheckboxInput, \
    PasswordInput, NumberInput
from django.forms import MultiWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from newadmin.utils import ChainedMultipleSelectWidget
from calendar import HTMLCalendar
from collections import OrderedDict
from datetime import datetime
import html
from django import forms


class TransferSelectWidget(SelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        options = []
        for choice in self.choices:
            options.append('{value:"%s", content:"%s"}' % (choice[0], choice[1]))
        selected = []
        if value:
            for pk in value:
                selected.append('"%s"' % pk)
        s = u'''
        <div id="__%s"></div>
        <script>
            $(function() {
                var t = $('#__%s').bootstrapTransfer(
                    {'target_id': '%s',
                     'height': '15em',
                     'hilite_selection': true});
                t.populate([%s]);
                t.set_values([%s]);
                //console.log(t.get_values());
            });
        </script>
        ''' % (name, name, name, ', '.join(options), ', '.join(selected))
        return mark_safe(s)


class ChainedTransferSelectWidget(ChainedMultipleSelectWidget):

    def render(self, name, value, attrs=None, choices=()):
        context = self.get_context(name, value, attrs, choices)
        context['name'] = name
        html = '<div id="__%s"></div>' % name
        output = [html, render_to_string('transferselect_widget.html', context)]
        return mark_safe('\n'.join(output))


class PhotoCaptureInput(HiddenInput):
    def render(self, name, value, attrs=None):
        s = u"""

        <div align="center">
            <video autoplay style="display:none;"></video>
            <canvas id="canvas" width="300" height="400"></canvas>
            <br>
            <input type="button" id="cancel" value="Cancelar" class="btn default">
            &nbsp;&nbsp;
            <input type="button" id="snapshot" value="Fotografar" class="btn primary">
        </div>

	<script language='javascript'>
		var video = document.querySelector("video");
		var canvas = document.querySelector("canvas");
		var canvas_visible = canvas.offsetParent != null;
		var ctx = canvas.getContext('2d');
		var t;
		var c = 0;

        if (canvas_visible){
		    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

    		if (navigator.getUserMedia) {
	    		navigator.getUserMedia({video: true}, handleVideo, videoError);
		    }
        }

		function handleVideo(stream) {
		    var createObjectURL = (window.URL || window.webkitURL || {}).createObjectURL || function(){};
			video.src = createObjectURL(stream);
		}

		function videoError(e) {
			ctx.font="20px Georgia";
			ctx.fillText("Nenhuma camera encontrada!",10,50);
		}
		function crop(){
			var sourceX = 200;
			var sourceY = 0;
			var sourceWidth = 300;
			var sourceHeight = 400;
			var destWidth = sourceWidth;
			var destHeight = sourceHeight;
			var destX = canvas.width / 2 - destWidth / 2;
			var destY = canvas.height / 2 - destHeight / 2;

			ctx.drawImage(video, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY, destWidth, destHeight);
		}
		function snapshot() {
			if(c == 0){
				crop();
				t = setTimeout("snapshot()", 100);
			}
		}

		if (canvas_visible){
            document.querySelector('#snapshot').onclick = function() {
                if(c == 0){
                    c = 1;
                    crop();
                    clearTimeout(t);
                    var dataURL = canvas.toDataURL();
                    hidden = document.querySelector("#id_%s");
                    hidden.value=dataURL;
                }
            }
            document.querySelector('#cancel').onclick = function() {
                if(c == 1){
                    c = 0;
                    hidden = document.querySelector("#id_%s");
                    hidden.value='';
                    snapshot();
                }
            }
		    snapshot();
		}
	</script>
        """ % (name, name)
        return mark_safe(s) + super(PhotoCaptureInput, self).render(name, value, attrs)


class RadioSelectClearable(RadioSelect):
    default_class = 'clearable-radio-input'

    def __init__(self, **kwargs):
        attrs = kwargs.get('attrs', {})
        if 'class' in attrs:
            attrs['class'] += f' {self.default_class}'
        else:
            attrs['class'] = self.default_class
        kwargs['attrs'] = attrs
        super().__init__(**kwargs)

    class Media:
        js = ('base/js/clearableradioinput.js',)


class NotApplicableRadioSelect(RadioSelect):
    default_class = 'not-applicable-radio'

    def __init__(self, when, target, **kwargs):
        attrs = kwargs.get('attrs', {})
        if 'class' in attrs:
            attrs['class'] += f' {self.default_class}'
        else:
            attrs['class'] = self.default_class
        attrs["data-not-applicable-radio-when"] = when
        attrs["data-not-applicable-radio-target"] = target
        kwargs['attrs'] = attrs
        super().__init__(**kwargs)

    class Media:
        js = ('base/js/notapplicableradioselect.js',)


class NumberScaleRadio(RadioSelect):
    default_class = 'number-scale-radio'

    def __init__(self, **kwargs):
        attrs = kwargs.get('attrs', {})
        if 'class' in attrs:
            attrs['class'] += f' {self.default_class}'
        else:
            attrs['class'] = self.default_class
        kwargs['attrs'] = attrs
        super().__init__(**kwargs)

    class Media:
        js = ('base/js/numberscaleradio.js',)
        css = {
            'screen': ('base/css/numberscaleradio.css',)
        }


class NotApplicableCheckboxInput(CheckboxInput):
    """
    Este widget deve ser usado em associação a outro campo alvo (target) para
    indicar que o valor dele (target) não se aplica.

    Seu comportamento passa a ser assim:
    - Quando o "Não se aplica" está vazio: o campo alvo é obrigatório e deve ser preenchido.
    - Quando o "Não se aplica" está marcado: o campo alvo é opcional e o valor dele fica vazio.

    Por exemplo: um campo de texto chamado "exames_anteriores" precisa de um campo
    "não se aplica" associado a ele, então, você deve criar da seguinte forma:

    exames_anteriores = forms.CharField(..., widget=TextInput())
    exames_anteriores_na = forms.BooleanField(
    ...
    widget=NotApplicableCheckboxInput(target="exames_anteriores")
    )

    Atenção:
    - O sufixo "_na" (abreviação de "não se aplica") é importante para que o
    estilo CSS funcione.
    - O parâmetro "target" é obrigatório e deve ser o nome exato do campo alvo
    para que o comportamento em Javascript funcione.
    - É necessário incluir {{ form.media.css }} no cabeçalho da página.
    - É necessário incluir {{ form.media.js }} no final da tag body da página.
    """
    default_class = 'not-applicable'

    def __init__(self, target, **kwargs):
        attrs = kwargs.get('attrs', {})
        if 'class' in attrs:
            attrs['class'] += f' {self.default_class}'
        else:
            attrs['class'] = self.default_class
        attrs["data-not-applicable-target"] = target
        kwargs['attrs'] = attrs
        super().__init__(**kwargs)

    class Media:
        js = ('base/js/notapplicablecheckboxinput.js',)
        css = {
            'screen': ('base/css/notapplicablecheckboxinput.css',)
        }


class Calendario(HTMLCalendar):
    meses_extenso = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    eventos = OrderedDict()
    eventos_por_mes = OrderedDict()
    tipos_eventos_calendario = OrderedDict()
    mostrar_mes_ano_cabecalho_mes = False

    def adicionar_tipo_evento(self, css, tipo_evento):
        if not css in self.tipos_eventos_calendario:
            self.tipos_eventos_calendario[css] = str(tipo_evento)

    def resetar_listas(self):
        self.eventos = OrderedDict()
        self.eventos_por_mes = OrderedDict()
        self.tipos_eventos_calendario = OrderedDict()
        self.tipos_eventos_calendario['hoje'] = 'Hoje'
        if self.tipos_eventos_default:
            self.tipos_eventos_calendario['evento'] = 'Evento/Data Comemorativa'
            self.tipos_eventos_calendario['extra'] = 'Liberação Por Documento Legal / Parcial'
            self.tipos_eventos_calendario['ferias'] = 'Férias'
            self.tipos_eventos_calendario['recesso'] = 'Recesso'
            self.tipos_eventos_calendario['feriado'] = 'Feriado'

    def __init__(self, firstweekday=6, tipos_eventos_default=True):
        self.firstweekday = firstweekday
        self.tipos_eventos_default = tipos_eventos_default
        self.resetar_listas()

    def retirar_numeros_string(self, valor):
        for num in range(0, 10):
            valor = valor.replace(str(num), "")
        return valor

    def existe_padrao_numerico(self, lista_css, padrao):
        lista = lista_css.split()
        for css in lista:
            css_padrao = self.retirar_numeros_string(css)
            css_padrao = css_padrao.split("_")[0]
            if css_padrao != padrao:
                return False
        return True

    def adicionar_evento_calendario(self, data_inicio, data_fim, descricao, css_class, title=''):
        """
        Metodo que montará o evento no calendario.
        """
        # Tratamento do CSS
        if data_inicio == data_fim:
            if self.eventos.get(str(data_inicio)):
                if not css_class in self.eventos.get(str(data_inicio))['css']:
                    self.eventos[str(data_inicio)]['css'] += ' ' + css_class

                if len(self.eventos.get(str(data_inicio))['css']) >= 2:
                    padrao_css = self.retirar_numeros_string(css_class)

                    if self.existe_padrao_numerico(self.eventos.get(str(data_inicio))['css'], self.retirar_numeros_string(css_class)):
                        if not "{}_conflito_leve".format(padrao_css) in self.eventos.get(str(data_inicio))['css']:
                            self.eventos[str(data_inicio)]['css'] += ' {}_conflito_leve'.format(padrao_css)
                        else:
                            self.eventos[str(data_inicio)]['css'] += ' {}_conflito_varios'.format(padrao_css)

                self.eventos[str(data_inicio)]['title'] += ' {}'.format(title)

            else:
                self.eventos[str(data_inicio)] = dict(data=data_inicio, css=css_class, title=title)

        elif data_fim:
            for data in daterange(data_inicio, data_fim):
                if self.eventos.get(str(data)):
                    if not css_class in self.eventos.get(str(data))['css']:
                        self.eventos[str(data)]['css'] += ' ' + css_class

                    if len(self.eventos.get(str(data))['css']) >= 2:
                        padrao_css = self.retirar_numeros_string(css_class)

                        if self.existe_padrao_numerico(self.eventos.get(str(data))['css'], self.retirar_numeros_string(css_class)):
                            if not "{}_conflito_leve".format(padrao_css) in self.eventos.get(str(data))['css']:
                                self.eventos[str(data)]['css'] += ' {}_conflito_leve'.format(padrao_css)
                            else:
                                self.eventos[str(data)]['css'] += ' {}_conflito_varios'.format(padrao_css)

                    self.eventos[str(data)]['title'] += ' | {}'.format(title)
                else:
                    self.eventos[str(data)] = dict(data=data, css=css_class, title=title)

        descricao = html.escape(descricao)
        #   Tratamento dos Eventos Verificar se as datas inicial e final estao no mesmo mês e ano
        if data_inicio and data_fim:
            if data_inicio.year == data_fim.year:
                if data_inicio.month == data_fim.month:
                    ano_mes = str(data_inicio.year) + str(data_inicio.month)
                    if not self.eventos_por_mes.get(ano_mes):
                        self.eventos_por_mes[ano_mes] = []
                    self.eventos_por_mes[ano_mes].append(dict(data_inicio=data_inicio, data_fim=data_fim, descricao=descricao, css=css_class, title=title))
                else:
                    for mes in range(data_inicio.month, data_fim.month + 1):
                        if not self.eventos_por_mes.get(str(data_inicio.year) + str(mes)):
                            self.eventos_por_mes[str(data_inicio.year) + str(mes)] = []
                        self.eventos_por_mes[str(data_inicio.year) + str(mes)].append(dict(data_inicio=data_inicio, data_fim=data_fim, descricao=descricao, css=css_class, title=title))
            else:
                for mes in range(data_inicio.month, 13):
                    if not self.eventos_por_mes.get(str(data_inicio.year) + str(mes)):
                        self.eventos_por_mes[str(data_inicio.year) + str(mes)] = []
                    self.eventos_por_mes[str(data_inicio.year) + str(mes)].append(dict(data_inicio=data_inicio, data_fim=data_fim, descricao=descricao, css=css_class, title=title))

                for mes in range(1, data_fim.month + 1):
                    if not self.eventos_por_mes.get(str(data_fim.year) + str(mes)):
                        self.eventos_por_mes[str(data_fim.year) + str(mes)] = []
                    self.eventos_por_mes[str(data_fim.year) + str(mes)].append(dict(data_inicio=data_inicio, data_fim=data_fim, descricao=descricao, css=css_class, title=title))

    def montar_dia(self, dia, dia_da_semana, mes, ano):
        """
        Retorna o dia como um tipo <td>
        """
        if dia == 0:
            return self.celula_do_dia('', '', '&nbsp;', dia_da_semana)
        else:
            cssclass = []
            titles = []
            hoje = datetime.now()
            if hoje.day == dia and hoje.month == mes and hoje.year == ano:
                cssclass.append('hoje')
            if dia_da_semana == 5 or dia_da_semana == 6:
                cssclass.append('fds')

            data = []
            data.append(str(dia))
            data.append(str(mes))
            data.append(str(ano))
            try:
                data = datetime.strptime('-'.join(data), "%d-%m-%Y").date()
                if self.eventos.get(str(data)):
                    cssclass.append(self.eventos[str(data)]['css'])
                    titles.append(self.eventos[str(data)].get('title') or self.eventos[str(data)]['css'].title())
            except Exception:
                pass
            return self.celula_do_dia(' '.join(cssclass), '&#13;'.join(titles), dia, dia_da_semana)  # '&#13;' quebra a linha no title

    def celula_do_dia(self, cssclass, titles, dia, dia_da_semana, conteudo=''):
        celula_dia = []
        if dia_da_semana == 0:
            semana = 'calendario-segunda'
        elif dia_da_semana == 1:
            semana = 'calendario-terca'
        elif dia_da_semana == 2:
            semana = 'calendario-quarta'
        elif dia_da_semana == 3:
            semana = 'calendario-quinta'
        elif dia_da_semana == 4:
            semana = 'calendario-sexta'
        elif dia_da_semana == 5:
            semana = 'calendario-sabado'
        elif dia_da_semana == 6:
            semana = 'calendario-domingo'
            celula_dia.append('<tr>')

        if dia:
            dia = '<span>%s</span>' % dia

        celula_dia.append('<td class="%s" title="%s" headers="%s">%s%s</td>' % (cssclass, titles, semana, dia, conteudo))
        if dia_da_semana == 5:
            celula_dia.append('</tr>')

        return '\n'.join(celula_dia)

    def montar_calendario_mes(self, mes, ano):
        html_code = ['<div class = "calendario">']
        html_code.append('<table class="calendario-dias">')
        if self.mostrar_mes_ano_cabecalho_mes:
            html_code.append('<caption>%s/%s</caption>' % (self.meses_extenso[int(mes) - 1], ano))
        else:
            html_code.append('<caption>%s</caption>' % self.meses_extenso[int(mes) - 1])

        html_code.append('<thead>')
        html_code.append('<tr>')
        html_code.append('<th id="calendario-domingo">Dom</th>')
        html_code.append('<th id="calendario-segunda">Seg</th>')
        html_code.append('<th id="calendario-terca">Ter</th>')
        html_code.append('<th id="calendario-quarta">Qua</th>')
        html_code.append('<th id="calendario-quinta">Qui</th>')
        html_code.append('<th id="calendario-sexta">Sex</th>')
        html_code.append('<th id="calendario-sabado">Sab</th>')
        html_code.append('</tr>')
        html_code.append('</thead>')
        html_code.append('<tbody>')
        return '\n'.join(html_code)

    def fechar_calendario_mes(self):
        html_code = ['</tbody></table>']
        return '\n'.join(html_code)

    def legenda_tipos_eventos(self):
        html_code = []
        html_code.append('<div class="legenda">')
        html_code.append('<p>Legenda:</p>')
        html_code.append('<ul>')
        for css_evento in self.tipos_eventos_calendario:
            html_code.append('<li class="%s">%s</li>' % (css_evento, self.tipos_eventos_calendario.get(css_evento)))

        html_code.append('</ul>')
        html_code.append('</div>')
        return '\n '.join(html_code)

    def fechar_div_calendario_mes(self):
        html_code = ['</div>']
        return '\n'.join(html_code)

    def montar_legenda(self, mes, ano):
        ano_mes = str(ano) + str(mes)
        if self.eventos_por_mes.get(ano_mes):
            html_code = ['<ul class="calendario-referencia">']
            #
            eventos = self.eventos_por_mes.get(ano_mes)
            eventos_clean = []
            for evento in eventos:
                if not (evento in eventos_clean):  # remove eventos IDÊNTICOS
                    eventos_clean.append(evento)
            eventos_clean = sorted(eventos_clean, key=lambda e: e['data_inicio'])  # ordena por data_inicio
            #
            for evento in eventos_clean:
                if evento['data_inicio'] == evento['data_fim'] or evento['data_fim'] is None:
                    html_code.append('<li class="%s">Dia %s: %s</li>' % (evento['css'], str(evento['data_inicio'].day), evento['descricao']))
                else:
                    html_code.append(
                        '<li class="%s">De %s/%s a %s/%s: %s</li>'
                        % (
                            evento['css'],
                            str(evento['data_inicio'].day),
                            str(evento['data_inicio'].month),
                            str(evento['data_fim'].day),
                            str(evento['data_fim'].month),
                            evento['descricao'],
                        )
                    )
            html_code.append('</ul>')
            return '\n'.join(html_code)
        return ' '

    def formato_mes(self, ano, mes):
        html_code = self.montar_calendario_mes(mes, ano)
        for semana in self.monthdays2calendar(ano, mes):
            for dia, dia_da_semana in semana:
                html_code += self.montar_dia(dia, dia_da_semana, mes, ano)

        html_code += self.fechar_calendario_mes()
        html_code += self.montar_legenda(mes, ano)
        html_code += self.fechar_div_calendario_mes()
        return html_code

    def formato_ano(self, ano):
        html_code = []
        html_code.append(self.legenda_tipos_eventos())
        for cont in range(12):
            if cont == 0:
                html_code.append(self.abrir_div_container())
            html_code.append(self.formato_mes(ano, cont + 1))
            if cont == 11:
                html_code.append(self.fechar_div_container())

        return ' '.join(html_code)

    def formato_ano_calendario_compras(self, ano):
        html_code = []
        for cont in range(12):
            if cont == 0:
                html_code.append(self.abrir_div_container())
            html_code.append(self.formato_mes(ano, cont + 1))
            if cont == 11:
                html_code.append(self.fechar_div_container())

        return ' '.join(html_code)

    def formato_periodo(self, mes_inicio, ano_inicio, mes_fim, ano_fim):
        html_code = []
        mes_inicial_ano = mes_inicio
        for ano in range(ano_inicio, ano_fim + 1):
            mes_final_ano = 12
            if ano == ano_fim:
                mes_final_ano = mes_fim

            for mes in range(mes_inicial_ano, mes_final_ano + 1):
                html_code.append(self.formato_mes(ano, mes))

            mes_inicial_ano = 1  # recomeça em janeiro

        return ' '.join(html_code)

    def abrir_div_container(self):
        html_code = []
        html_code.append('<div class="calendarios-container">')
        return ' '.join(html_code)

    def fechar_div_container(self):
        html_code = []
        html_code.append('</div>')
        return ' '.join(html_code)

    def __str__(self):
        return self.formato_ano(datetime.today().year)


class CalendarioPlus(Calendario):
    mostrar_mes_e_ano = False  # cabeçalho do calendário de um mês --> ex.'Outubro/2013' ou 'Outubro'
    destacar_hoje = True
    destacar_fim_de_semana = True
    ocultar_titles_dia = False
    ocultar_legenda_eventos = False
    envolve_mes_em_um_box = False

    def adicionar_evento_calendario(self, data_inicio, data_fim, descricao, css_class, title=None, dia_todo=None, url=None):
        """
        Metodo que montará o evento no calendario.
        """
        # garante que as datas serão do tipo datetime
        if not type(data_inicio) is datetime:
            # redefine data_inicio
            data_inicio = datetime(data_inicio.year, data_inicio.month, data_inicio.day, 0, 0, 0)  # hour,minute,second

        if not data_fim:
            data_fim = data_inicio
        else:
            if not type(data_fim) is datetime:
                # redefine data_fim
                data_fim = datetime(data_fim.year, data_fim.month, data_fim.day, 0, 0, 0)  # hour,minute,second

        # nesse ponto, as datas são datetime

        '''
            eventos = {'todos': [{},{},{}],
                       'ano-mes': [{},{},{}]}
            evento = {
                        'data_inicio': dia/mes/ano hora:min:sec,
                        'data_fim': dia/mes/ano hora:min:sec,
                        'descricao_evento': 'evento 1',
                        'css_class': 'css_class 1',
                        'title': '?',
                        'url': None
                     }

            'ano-mes' obtido de data_inicio

            ** possibilidade de eventos paralelos em um mesmo dia

            Montando o mês:
             _____________
            |  mês[/ano]  |
             -------------
            | dias        |
             -------------

            Montando o dia:
                - hoje?
                    [css hoje]
                - fim de semana?
                    [css fds]
                - aplicar css_class do último evento (por enquanto 09/10/2013)
                    - eventos do dia/mês/ano --> eventos['todos'][evento X][data_inicio] <= dia/mes/ano <= eventos['todos'][evento X][data_fim]
                        - último evento
                            - aplicar css_class
                - [titles]
                    - eventos do dia/mês/ano --> eventos['todos'][evento X][data_inicio] <= dia/mes/ano <= eventos['todos'][evento X][data_fim]
                        - para cada evento
                            - concatena 'title' ou 'css_class'
                    - aplica concatenação

            [Montando a legenda do mês]
                - eventos do mês/ano --> eventos['ano-mes']
                    - para cada evento
                        - data_inicio = data_fim
                            - Dia X[,hora:min inicio à hora:min fim]: descricao_evento
                        - data_inicio <> data_fim
                            - mesmo mês?
                                - Dia X[, hora:min inicio] até Dia Y[, hora:min fim]: descricao_evento
                            - meses diferentes
                                - Dia X/mês A[, hora:min inicio] até Dia Y/mês B[, hora:min fim]: descricao_evento
                        - aplica css_class

            obtendo calendários:
                - obter calendário de um mês específico (mes/ano)
                    - monta o mês/ano
                - obter calendários de um ano específico (ano)
                    monta o ano
                        monta jan/ano
                        monta fev/ano
                        ...
                        monta dez/ano
                - obter calendários de um período específico (mes/ano inicio, mes/ano fim)
        '''

        evento = dict(data_inicio=data_inicio, data_fim=data_fim, descricao_evento=descricao, css_class=css_class, title=title, dia_todo=dia_todo, url=url)
        # todos
        if 'todos' not in self.eventos:
            self.eventos['todos'] = []
        self.eventos['todos'].append(evento)

        # por mês
        ano_mes = str(data_inicio.date().year) + str(data_inicio.date().month)
        if ano_mes not in self.eventos:
            self.eventos[ano_mes] = []
        self.eventos[ano_mes].append(evento)

    def eventos_da_data(self, data):
        eventos = []
        if 'todos' in self.eventos:
            # garante que 'data' seja um 'date'
            if type(data) is datetime:
                data = data.date()
            for evento in self.eventos['todos']:
                if data >= evento['data_inicio'].date() and data <= evento['data_fim'].date():
                    eventos.append(evento)
        return eventos

    def montar_dia(self, dia, dia_da_semana, mes, ano):
        """
        Retorna o dia como um tipo <td>
        """
        if dia == 0:
            return self.celula_do_dia('vazio', '', '', dia_da_semana)
        else:
            cssclass = set()
            if self.destacar_hoje:
                hoje = datetime.now()
                if hoje.day == dia and hoje.month == mes and hoje.year == ano:
                    cssclass.add('hoje')

            if self.destacar_fim_de_semana:
                if dia_da_semana == 5 or dia_da_semana == 6:
                    cssclass.add('fds')

            data = []
            data.append(str(dia))
            data.append(str(mes))
            data.append(str(ano))
            data = datetime.strptime('-'.join(data), "%d-%m-%Y").date()
            eventos = sorted(self.eventos_da_data(data), key=lambda e: e['data_inicio'])
            cssclass.add(self.eh_dia_todo(eventos, data))
            conteudo = self.montar_eventos(eventos)
            return self.celula_do_dia(' '.join(cssclass), '', dia, dia_da_semana, conteudo)

    def eh_dia_todo(self, eventos, data):
        if len(eventos) <= 1:
            for evento in eventos:
                if evento['dia_todo']:
                    return evento['css_class']

        return ''

    def qtd_cssclass(self, cssclass):
        """
        Retorna a quantidade de classes dos eventos, ou seja, excluindo os colocados pelo calendário (hoje e fds)
        """
        cssclass_extra = cssclass.copy()
        cssclass_extra.discard('hoje')
        cssclass_extra.discard('fds')
        return len(cssclass_extra)

    def montar_calendario_mes(self, mes, ano):
        html_code = ['<div class="calendario calendario-mensal">']
        html_code.append('<table>')
        if not self.envolve_mes_em_um_box:
            if self.mostrar_mes_e_ano:
                html_code.append('<caption>%s/%s</caption>' % (self.meses_extenso[int(mes) - 1], ano))
            else:
                html_code.append('<caption>%s</caption>' % self.meses_extenso[int(mes) - 1])
        html_code.append('<thead>')
        html_code.append('<tr>')
        html_code.append('<th class="semana">Dom</th>')
        html_code.append('<th class="semana">Seg</th>')
        html_code.append('<th class="semana">Ter</th>')
        html_code.append('<th class="semana">Qua</th>')
        html_code.append('<th class="semana">Qui</th>')
        html_code.append('<th class="semana">Sex</th>')
        html_code.append('<th class="semana">Sab</th>')
        html_code.append('</tr>')
        html_code.append('</thead>')
        html_code.append('<tbody>')
        return '\n'.join(html_code)

    def montar_eventos(self, eventos):
        legendas = list()
        for evento in eventos:
            descricao = evento['descricao_evento']
            url = evento.get('url')
            extra = url and 'style="cursor:pointer" onclick="popup(\'{}\')"'.format(url) or ''
            legendas.append('<li %s class="%s" title="%s">%s</li>' % (extra, evento['css_class'], evento['title'], descricao))

        html_code = ['<ul class="calendario-referencia">'] + legendas + ['</ul>']
        return '\n'.join(html_code)

    def formato_mes(self, ano, mes):
        html_code = self.montar_calendario_mes(mes, ano)
        for semana in self.monthdays2calendar(ano, mes):
            for dia, dia_da_semana in semana:
                html_code += self.montar_dia(dia, dia_da_semana, mes, ano)
        html_code += self.fechar_calendario_mes()
        html_code += self.fechar_div_calendario_mes()
        if self.envolve_mes_em_um_box:
            if self.mostrar_mes_e_ano:
                title_box = '{}/{}'.format(self.meses_extenso[int(mes) - 1], ano)
            else:
                title_box = '{}'.format(self.meses_extenso[int(mes) - 1])
            html_code = '<div class="box"><h3>{}</h3>{}</div>'.format(title_box, html_code)
        return html_code

    def formato_periodo(self, mes_inicio, ano_inicio, mes_fim, ano_fim, omite_mes_sem_eventos=False):
        html_code = []
        mes_inicial_ano = mes_inicio
        for ano in range(ano_inicio, ano_fim + 1):
            mes_final_ano = 12
            if ano == ano_fim:
                mes_final_ano = mes_fim
            for mes in range(mes_inicial_ano, mes_final_ano + 1):
                if omite_mes_sem_eventos:
                    omite_mes = True
                    for evento in self.eventos['todos']:
                        if evento['data_inicio'].month == mes and evento['data_inicio'].year == ano or evento['data_fim'].month == mes and evento['data_fim'].year == ano:
                            omite_mes = False
                            break
                    if omite_mes:
                        continue
                #
                html_code.append(self.formato_mes(ano, mes))
            mes_inicial_ano = 1  # recomeça em janeiro
        return ' '.join(html_code)


class Cid10ModelSelect2MultipleWidget(ModelSelect2MultipleWidget):
    """
    Este componente foi criado para personalizar o label de apresentação do Cid10
    """
    def label_from_instance(self, obj):
        return f"{obj.nome} ({obj.codigo})"


class Cid10ModelSelect2Widget(ModelSelect2Widget):
    """
    Este componente foi criado para personalizar o label de apresentação do Cid10
    """
    def label_from_instance(self, obj):
        return f"{obj.nome} ({obj.codigo})"


class CuidadoModelSelect2MultipleWidget(ModelSelect2MultipleWidget):
    """
    Este componente foi criado para personalizar o label de apresentação de Cuidado
    """
    def label_from_instance(self, obj):
        return f"{obj.descricao}"


class CuidadoModelSelect2Widget(ModelSelect2Widget):
    """
    Este componente foi criado para personalizar o label de apresentação de Cuidado
    """
    def label_from_instance(self, obj):
        return f"{obj.descricao}"



class PinCode(MultiWidget):
    """
    Um widget que representa um Pin Code, ou seja, um código de n dígitos que é exibido em inputs separados
    """

    template_name = "forms/widgets/pincode.html"

    def __init__(self, attrs=None, pin_length=4):
        self.pin_length = pin_length
        attrs = {**(attrs or {}), 'maxlength': 1, 'autocomplete': 'new-password'}
        widgets = tuple(PasswordInput(attrs=attrs) for i in range(self.pin_length))
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            if isinstance(value, str) and len(value) == self.pin_length:
                return list(value)
        return list(i for i in range(self.pin_length))

    class Media:
        js = ('base/js/pin-code.js',)
        css = {
            'screen': ('base/css/pin-code.css',)
        }


class BloodPressure(MultiWidget):
    template_name = "forms/widgets/blood_pressure.html"

    def __init__(self, attrs=None, systolic_attrs=None, diastolic_attrs=None):
        self.systolic_attrs = {} if systolic_attrs is None else systolic_attrs.copy()
        self.diastolic_attrs = {} if diastolic_attrs is None else diastolic_attrs.copy()
        attrs = {} if attrs is None else attrs.copy()
        widgets = (
            NumberInput(attrs={**attrs, **self.systolic_attrs}),
            NumberInput(attrs={**attrs, **self.diastolic_attrs})
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            if isinstance(value, str):
                return value.split("x")
        return None, None


class DateTimeWidget(forms.SplitDateTimeWidget):
    template_name = "forms/widgets/splitdatetime.html"
    date_grid = 7
    time_grid = 5

    def __init__(self, date_grid=None, time_grid=None, **kwargs):
        super().__init__(**kwargs)
        if date_grid is not None:
            self.date_grid = date_grid
        if time_grid is not None:
            self.time_grid = time_grid

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        subwidgets = context['widget']['subwidgets']
        subwidgets[0]["grid"] = self.date_grid
        subwidgets[1]["grid"] = self.time_grid
        return context
