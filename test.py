//This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivs License. License : https://creativecommons.org/licenses/by-nc-nd/4.0/
//@version=5
// © RickSimpson

indicator(title="Tailored-Custom Hamonic Patterns", shorttitle='T-C Harmonic Patterns', overlay=true)

//Original Bat Pattern work by Scott M.Carney. More information on : https://harmonictrader.com/harmonic-patterns/bat-pattern/ - Original Butterfly Pattern work by Bryce Gilmore. More information on : https://harmonictrader.com/harmonic-patterns/butterfly-pattern/ - Original Gartley Pattern work by H.M.Gartley. More information on : https://harmonictrader.com/harmonic-patterns/Gartley-pattern/

//◀─── Groups Setup ───►

ghp = 'Harmonic Patterns Settings'
gbs = 'Bands Settings'
gro = 'XAB/ABC Ratios Settings'
gpn = 'Projections Settings'
gtl = 'Targets Levels Settings'
grl = 'Ratio Settings'
gbt = 'Backtesting Settings'

//◀─── Constants Arrays Declaration ───►

pattern_names    = array.from('i_pattern1', 'i_pattern2', 'i_pattern3')
int pattern_size = array.size(pattern_names)

//◀─── Inputs ───►

i_pattern1            = input.bool(true,                'Pattern 1',                                                                                                                                 group=ghp, inline='pattern')
i_pattern2            = input.bool(true,                'Pattern 2',                                                                                                                                 group=ghp, inline='pattern')
i_pattern3            = input.bool(true,                'Pattern 3',                                                                                                                                 group=ghp, inline='pattern')
i_p1id                = input.string('Bat',             'Pattern 1 Name',                                                                                                                            group=ghp)
i_p2id                = input.string('Butterfly',       'Pattern 2 Name',                                                                                                                            group=ghp)
i_p3id                = input.string('Gartley',         'Pattern 3 Name',                                                                                                                            group=ghp)
i_bullishclr          = input.color(color.teal,       'Bullish Pattern Color',                                                                                                                     group=ghp, inline='hpcstyle')
i_bearishclr          = input.color(color.red,        'Bearish Pattern Color',                                                                                                                     group=ghp, inline='hpcstyle')
i_bgfilling           = input.float(95,                 'Pattern Background Filling                         ',                                                                                       group=ghp)
i_hpstyle             = input.string('Solid',           'Lines Style',                        options=['Solid', 'Dotted', 'Dashed'],                                                                 group=ghp, inline='hpltyle')
i_hpwidth             = input.int(1,                    'Lines Width',          minval=1,                                                                                                            group=ghp, inline='hpltyle')
i_hpminlen            = input.int(5,                    'Min Length',           minval=2,                maxval=50,                                                                                  group=ghp, inline='Length')
i_hpmaxlen            = input.int(20,                   'Max Length',           minval=2,                maxval=50,                                                                                  group=ghp, inline='Length')
i_hpdynperc           = input.float(96.85,              'Dynamic Length Adaptive Percentage', minval=0,  maxval=100,                                                                                 group=ghp) / 100.0
i_uc                  = input.bool(false,               'Use Close Price?',                                                                                                                          group=ghp)
i_bc                  = input.bool(true,                'Bar Color?',                                                                                                                                group=ghp)
i_maxpvs              = input.int(300,                  'Max Pivot Size',                     step=1,                                                                                                group=ghp)
i_showbands           = input.bool(true,                'Show Bands?',                                                                                                                               group=gbs)
i_upchanclr           = input.color(color.teal,       'Upper Color',                                                                                                                               group=gbs, inline='bandsstyle')
i_michanclr           = input.color(color.gray,       'Middle Color',                                                                                                                              group=gbs, inline='bandsstyle')
i_lochanclr           = input.color(color.red,        'Lower Color',                                                                                                                               group=gbs, inline='bandsstyle')
i_chantransp          = input.float(90,                 'Channel Background Filling                         ',                                                                                       group=gbs)
i_calctype            = input.string('Bollinger Bands', 'Calculation Type',                   options=['Bollinger Bands', 'Keltner Channel', 'Donchian Channel'],                                    group=gbs)
i_matype              = input.string('SMA',             'Filter Type',                        options=['SMA', 'EMA', 'HMA', 'RMA', 'WMA', 'VWMA', 'HIGH/LOW', 'LINREG', 'MEDIAN'],                   group=gbs)
i_multiplier          = input.float(2.0,                'Multiplier',           minval=0.5,   step=0.5,                                                                                              group=gbs)
i_sticky              = input.bool(true,                'Sticky Bands?',                                                                                                                             group=gbs)
i_adaptive            = input.bool(true,                'Adaptive Length?',                                                                                                                          group=gbs)
i_bullpattern1min     = input.float(0.382,              'Pattern 1 Minimum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bullpattern1max     = input.float(0.5,                'Pattern 1 Maximum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern1min     = input.float(0.382,              'Pattern 1 Minimum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern1max     = input.float(0.886,              'Pattern 1 Maximum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bullpattern2min     = input.float(0.786,              'Pattern 2 Minimum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bullpattern2max     = input.float(0.786,              'Pattern 2 Maximum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern2min     = input.float(0.382,              'Pattern 2 Minimum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern2max     = input.float(0.886,              'Pattern 2 Maximum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bullpattern3min     = input.float(0.618,              'Pattern 3 Minimum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bullpattern3max     = input.float(0.618,              'Pattern 3 Maximum XAB Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern3min     = input.float(0.382,              'Pattern 3 Minimum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_bearpattern3max     = input.float(0.886,              'Pattern 3 Maximum ABC Ratio',        options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gro)
i_showprojections     = input.bool(true,                'Displays Leg Projections Lines?',                                                                                                           group=gpn)
i_extendprojections   = input.bool(true,                'Extends Leg Projections Lines?',                                                                                                            group=gpn)
i_pattern1projbdratio = input.float(0.886,              'BD Leg Pattern 1 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_pattern1projcdratio = input.float(0.886,              'CD Leg Pattern 1 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_pattern2projbdratio = input.float(1.272,              'BD Leg Pattern 2 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_pattern2projcdratio = input.float(1.272,              'CD Leg Pattern 2 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_pattern3projbdratio = input.float(0.786,              'BD Leg Pattern 3 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_pattern3projcdratio = input.float(0.786,              'CD Leg Pattern 3 Projections Ratio', options=[.0146, .236, .382, .5, .618, .786, .886, .901, 1., 1.272, 1.414, 1.618, 2.436, 2.618, 3.618], group=gpn)
i_showtargets         = input.bool(true,                'Show Targets?',                                                                                                                             group=gtl)
i_extendstargets      = input.bool(true,                'Extends Targets Lines?',                                                                                                                    group=gtl)
i_targetstxtsize      = input.string('Small',           'Targets Text Size',                  options=['Tiny', 'Small', 'Normal', 'Large', 'Huge', 'Auto'],                                          group=gtl)
i_stoploss            = input.float(-2.5,               'Stop-Loss  [%]',       minval=-100,  step=0.05, maxval=100,                                                                                 group=gtl, inline='SL') * 0.01
i_stoplossclr         = input.color(color.red,        '',                                                                                                                                          group=gtl, inline='SL')
i_prz                 = input.float(0.0,                'PRZ              [%]', minval=0,     step=1,    maxval=100,                                                                                 group=gtl, inline='D') * 0.01
i_przclr              = input.color(color.silver,     '',                                                                                                                                          group=gtl, inline='D')
i_target1             = input.float(23.6,               'Target 1       [%]',   minval=0,     step=1,    maxval=100,                                                                                 group=gtl, inline='T1') * 0.01
i_target1clr          = input.color(color.teal,       '',                                                                                                                                          group=gtl, inline='T1')
i_target2             = input.float(50.0,               'Target 2     [%]',     minval=0,     step=1,    maxval=100,                                                                                 group=gtl, inline='T2') * 0.01
i_target2clr          = input.color(color.orange,     '',                                                                                                                                          group=gtl, inline='T2')
i_target3             = input.float(61.8,               'Target 3     [%]',     minval=0,     step=1,    maxval=100,                                                                                 group=gtl, inline='T3') * 0.01
i_target3clr          = input.color(color.teal,       '',                                                                                                                                          group=gtl, inline='T3')
i_target4             = input.float(78.6,               'Target 4     [%]',     minval=0,     step=1,    maxval=100,                                                                                 group=gtl, inline='T4') * 0.01
i_target4clr          = input.color(color.teal,       '',                                                                                                                                          group=gtl, inline='T4')
i_ratioslabels        = input.bool(true,                'Show Ratios Labels?   ',                                                                                                                    group=grl, inline='ratiolabelstyle')
i_ratioslabelsclr     = input.color(color.silver,     '',                                                                                                                                          group=grl, inline='ratiolabelstyle')
i_ratioslines         = input.bool(true,                'Displays Ratios Lines?',                                                                                                                    group=grl, inline='ratiolinestyle')
i_ratioclr            = input.color(color.silver,     '',                                                                                                                                          group=grl, inline='ratiolinestyle')
i_ratioprecision      = input.int(16,                   'Ratio Precision [%]',  minval=1,     step=1,    maxval=50,                                                                                  group=grl)
i_ratiotxtsize        = input.string('Normal',          'Text Size',                          options=['Tiny', 'Small', 'Normal', 'Large', 'Huge', 'Auto'],                                          group=grl)
i_ratiostyle          = input.string('Dotted',          'Lines Style',                        options=['Solid', 'Dotted', 'Dashed'],                                                                 group=grl)
i_ratiolineswidth     = input.int(1,                    'Lines Width',          minval=1,                                                                                                            group=grl)
i_showtable           = input.bool(true,                'Display Backtesting Table?',                                                                                                                group=gbt)
i_tablepos            = input.string('Bottom Left',     'Table Position',                     options=['Top Left', 'Top Center', 'Top Right', 'Bottom Left', 'Bottom Center', 'Bottom Right'],       group=gbt)

//◀─── Variables Declarations───►

var       trend         = 0
var       current_trend = 0
var       currentdir    = 0
var int   counter       = 6
var float upper         = 0.0
var float lower         = 0.0
var float middle        = 0.0
var       pivots        = array.new_float(0)
var       pivotscount   = array.new_int(0)
var       pivotsdir     = array.new_int(0)
var       patternlines  = array.new_line(6)
var       patterntype   = array.new_int(2,                 1)
var       patternlabels = array.new_bool(pattern_size, false)
var       patnewlabel   = array.new_label(1)
var       leg           = array.new_label(6)
var       ratiolines    = array.new_line(5)
var       ratios        = array.new_label(5)
var       targets       = array.new_line(6)
var       targetslabels = array.new_label(6)
var       bearstate     = array.new_int(pattern_size,      0)
var       bullstate     = array.new_int(pattern_size,      0)

//◀─── Size Adjustment String Calculation ───►

tleveladjustment   = i_targetstxtsize == 'Tiny'     ? size.tiny         : i_targetstxtsize == 'Small'      ? size.small          : i_targetstxtsize == 'Normal'    ? size.normal        : i_targetstxtsize == 'Large'       ? size.large           : i_targetstxtsize == 'Huge'          ? size.huge              : i_targetstxtsize == 'Auto'         ? size.auto             : na
lpatternadjustment = i_ratiotxtsize   == 'Tiny'     ? size.tiny         : i_ratiotxtsize   == 'Small'      ? size.small          : i_ratiotxtsize   == 'Normal'    ? size.normal        : i_ratiotxtsize   == 'Large'       ? size.large           : i_ratiotxtsize   == 'Huge'          ? size.huge              : i_ratiotxtsize   == 'Auto'         ? size.auto             : na

//◀─── Style Adjustment String Calculation ───►

patternlinestyle   = i_hpstyle        == 'Dotted'   ? line.style_dotted : i_hpstyle        == 'Dashed'     ? line.style_dashed   : line.style_solid
ratiolinestyle     = i_ratiostyle     == 'Dotted'   ? line.style_dotted : i_ratiostyle     == 'Dashed'     ? line.style_dashed   : line.style_solid
tablepos           = i_tablepos       == 'Top Left' ? position.top_left : i_tablepos       == 'Top Center' ? position.top_center : i_tablepos       == 'Top Right' ? position.top_right : i_tablepos       == 'Bottom Left' ? position.bottom_left : i_tablepos       == 'Bottom Center' ? position.bottom_center : i_tablepos       == 'Bottom Right' ? position.bottom_right : na

//◀─── Bands Calculation ───►

//Global Functions

bandwidth_f(float    middle, float upper, float lower) => 100 * (upper  - lower) / middle
percentb_f(float     source, float upper, float lower) => 100 * (source - lower) / (upper - lower)
customseries_f(float source=close, simple string type='SMA', simple int length) =>
    switch type
    	'EMA'     => ta.ema(source,        length)
    	'SMA'     => ta.sma(source,        length)
    	'RMA'     => ta.rma(source,        length)
    	'HMA'     => ta.hma(source,        length)
    	'WMA'     => ta.wma(source,        length)
    	'VWMA'    => ta.vwma(source,       length)
    	'LINGREG' => ta.linreg(source,     length,    0)
    	'MEDIAN'  => ta.median(source,     length)
    	=> (ta.highest(length) + ta.lowest(length)) / 2

sticky_f(float highsource, float lowsource, float upper, float lower, simple bool i_sticky=false) =>
    newupper     = upper
    newlower     = lower
    highbreakout = highsource[1] >= newupper[1]
    lowbreakout  = lowsource[1]  <= newlower[1]
    newupper    := (highbreakout or lowbreakout or not i_sticky) ? newupper : nz(newupper[1], newupper)
    newlower    := (highbreakout or lowbreakout or not i_sticky) ? newlower : nz(newlower[1], newlower)
    [newupper, newlower]

ma_f(float     source=close, simple string i_matype='SMA', simple int length) =>
    customseries_f(source, i_matype, length)

atr_f(simple string                        i_matype='SMA', simple int length) =>
    customseries_f(ta.tr,  i_matype, length)

atrperc_f(simple string                    i_matype='SMA', simple int length) =>
    100 * atr_f(i_matype,            length) / close

bb_f(float     source=close, simple string i_matype='SMA', simple int length=50, float i_multiplier=2.0,                             simple bool i_sticky=false) =>
    float middle         = ma_f(source, i_matype,    length)
	float upper          = middle + ta.stdev(source, length) * i_multiplier
	float lower          = middle - ta.stdev(source, length) * i_multiplier
	[newupper, newlower] = sticky_f(high, low, upper, lower, i_sticky)
	upper               := newupper
	lower               := newlower
	[middle, upper, lower]

bbw_f(float    source=close, simple string i_matype='SMA', simple int length=50, float i_multiplier=2.0,                             simple bool i_sticky=false) =>
    [middle, upper, lower] = bb_f(source, i_matype, length, i_multiplier, i_sticky)
    bandwidth_f(middle, upper, lower)

bbperc_f(float source=close, simple string i_matype='SMA', simple int length=50, float i_multiplier=2.0,                             simple bool i_sticky=false) =>
    [middle, upper, lower] = bb_f(source, i_matype, length, i_multiplier, i_sticky)
    percentb_f(source,  upper, lower)

kc_f(float     source=close, simple string i_matype='EMA', simple int length=50, float i_multiplier=2.0, simple bool truerange=true, simple bool i_sticky=false) =>
    float middle         = ma_f(source, i_matype, length)
	float span           = (truerange) ? ta.tr : (high - low)
	float marng          = ma_f(span,   i_matype, length)
	float upper          = middle + marng * i_multiplier
	float lower          = middle - marng * i_multiplier
	[newupper, newlower] = sticky_f(high, low, upper, lower, i_sticky)
	upper               := newupper
	lower               := newlower
	[middle, upper, lower]

kcw_f(float    source=close, simple string i_matype='EMA', simple int length=50, float i_multiplier=2.0, simple bool truerange=true, simple bool i_sticky=false) =>
    [middle, upper, lower] = kc_f(source, i_matype, length, i_multiplier, truerange, i_sticky)
    bandwidth_f(middle, upper, lower)

kcperc_f(float source=close, simple string i_matype='EMA', simple int length=50, float i_multiplier=2.0, simple bool truerange=true, simple bool i_sticky=false) =>
    [middle, upper, lower] = kc_f(source, i_matype, length, i_multiplier, truerange, i_sticky)
    percentb_f(source,  upper, lower)

dc_f(simple     int length=50, simple bool altsrc=false, float alternatesource=close, simple bool i_sticky=false) =>
    highsource     = altsrc ? alternatesource : high
    lowsource      = altsrc ? alternatesource : low
    [upper, lower] = sticky_f(highsource, lowsource, ta.highest(highsource, length), ta.lowest(lowsource, length), i_sticky)
    middle         = (upper + lower) / 2
    [middle, upper, lower]

dcw_f(simple    int length=50, simple bool altsrc=false, float alternatesource=close, simple bool i_sticky=false) =>
    [middle, upper, lower] = dc_f(length, altsrc, alternatesource, i_sticky)
    bandwidth_f(middle, upper, lower)

dcperc_f(simple int length=50, simple bool altsrc=false, float alternatesource=close, simple bool i_sticky=false) =>
    [middle, upper, lower] = dc_f(length, altsrc, alternatesource, i_sticky)
    percentb_f(altsrc ? alternatesource : hl2, upper, lower)

oscillator_f(float source, simple string method='HIGH/LOW', simple int highlowlength=50, simple int rnglength=14, simple bool i_sticky=false) =>
    oschighest    = customseries_f(source,                            'HIGH',      highlowlength)
    osclowest     = customseries_f(source,                            'LOW',       highlowlength)
    oscoverbought = customseries_f(oschighest, method == 'HIGH/LOW' ? 'LOW'  : method, rnglength)
    oscoversold   = customseries_f(osclowest,  method == 'HIGH/LOW' ? 'HIGH' : method, rnglength)
    sticky_f(source, source, oscoverbought, oscoversold, i_sticky)

oscillator(simple string type='rsi', simple int length=14, simple int shortLength=13, simple int longLength=25, simple int highlowlength=50, float source=close, float highsource=high, float lowsource=low, simple string method='HIGH/LOW', simple bool sticky=false) =>
    oscillator =  ta.rsi(source, length)
    [overbought, oversold] = oscillator_f(oscillator, method, highlowlength, length, sticky)
    [oscillator, overbought, oversold]

multibands_f(simple string i_calctype='bb', float source=close, simple string i_matype='SMA', simple int length=150, simple bool truerange=true, simple bool i_sticky=false, simple int bandsnumber=7, simple float multiplierstart=0.5, simple float multiplierstep=0.5) =>
    bands = array.new_float()
    for i = 0 to bandsnumber -1
        i_multiplier  = multiplierstart + i * multiplierstep
        middle        = 0.0
        upper         = 0.0
        lower         = 0.0
        if(i_calctype == 'bb')
            [bbmiddle, bbupper, bblower] = bb_f(source, i_matype, length, i_multiplier,            i_sticky)
            middle   := bbmiddle
            upper    := bbupper
            lower    := bblower
        else
            [kcmiddle, kcupper, kclower] = kc_f(source, i_matype, length, i_multiplier, truerange, i_sticky)
            middle   := kcmiddle
            upper    := kcupper
            lower    := kclower
        array.unshift(bands, lower)
        array.unshift(bands, upper)
        if (i == 0)
            array.unshift(bands, middle)
    array.sort(bands)
    bands

rbandsosc_f(simple string i_calctype='kc', float source=close, simple string i_matype='SMA', simple int length=150, simple bool truerange=false, simple bool stickyband=false, simple int bandsnumber=100, simple float multiplierstart=0.5, simple float multiplierstep=0.5) =>
    states                = multibands_f(i_calctype, source, i_matype, length, truerange, stickyband, bandsnumber, multiplierstart, multiplierstep)
    currentstate          = array.size(states)
    for i                 = 0 to array.size(states) - 1 by 1
        if source < array.get(states, i)
            currentstate := i
            break
    currentstate

//Oscillator Calculation

if (i_calctype ==  'Bollinger Bands')
    [bmiddle, bupper, blower] = bb_f(close, i_matype, i_hpmaxlen, i_multiplier,       i_sticky)
    upper  := bupper
    lower  := blower
    middle := bmiddle

if (i_calctype ==  'Keltner Channel')
    [kmiddle, kupper, klower] = kc_f(close, i_matype, i_hpmaxlen, i_multiplier, true, i_sticky)
    upper  := kupper
    lower  := klower
    middle := kmiddle

if (i_calctype == 'Donchian Channel')
    [dmiddle, dupper, dlower] = dc_f(i_hpmaxlen, false, close,                        i_sticky)
    upper  := dupper
    lower  := dlower
    middle := dmiddle

//Conditions Calculation

var upperstate = nz(upper)
var lowerstate = nz(lower)
upperstate    := currentdir >= 0 or not i_adaptive ? upper : math.min(upper, upperstate)
lowerstate    := currentdir <= 0 or not i_adaptive ? lower : math.max(lower, lowerstate)

//Boolean Conditions To Float

var float upperstatefloat = na
if upperstate
    upperstatefloat      := bar_index
    upperstatefloat
var float lowerstatefloat = na
if lowerstate
    lowerstatefloat      := bar_index
    lowerstatefloat

//Bands Plotting

plot(i_showbands ? upperstate : na, 'Upper', i_upchanclr, 0, plot.style_linebr)
plot(i_showbands ? lowerstate : na, 'Lower', i_lochanclr, 0, plot.style_linebr)

//Channels Plotting

upperchannel  = plot(i_showbands ? upper  : na, title='Upper Channel',         color=i_upchanclr, linewidth=1, style=plot.style_linebr)
middlechannel = plot(i_showbands ? middle : na, title='Middle Channel',        color=i_michanclr, linewidth=1, style=plot.style_linebr)
lowerchannel  = plot(i_showbands ? lower  : na, title='Lower Channel',         color=i_lochanclr, linewidth=1, style=plot.style_linebr)
fill(upperchannel,  middlechannel,              title='Upper Channel Filling', color=color.new(i_upchanclr,              i_chantransp))
fill(middlechannel, lowerchannel,               title='Lower Channel Filling', color=color.new(i_lochanclr,              i_chantransp))

//Bands Channels Labels Plotting

if i_showbands and upperstatefloat
    l1 = label.new(bar_index, i_calctype == 'Bollinger Bands' ? upper  : i_calctype ==  'Keltner Channel' ? upper  : i_calctype == 'Donchian Channel' ? upper  : na, i_calctype == 'Bollinger Bands' ? 'BB +1 : ' + str.tostring(math.round_to_mintick(upper)) : i_calctype == 'Keltner Channel' ? 'KC +1 : ' + str.tostring(math.round_to_mintick(upper)) : i_calctype == 'Donchian Channel' ? 'DC +1 : ' + str.tostring(math.round_to_mintick(upper)) : na, yloc=yloc.price, color=color.new(i_upchanclr, 100), textcolor=color.new(i_upchanclr, 0), style=label.style_label_left, size=size.small)
    l1
    label.delete(l1[1])

if i_showbands and middle
    l2 = label.new(bar_index, i_calctype == 'Bollinger Bands' ? middle : i_calctype ==  'Keltner Channel' ? middle : i_calctype == 'Donchian Channel' ? middle : na, i_calctype == 'Bollinger Bands' ? 'BB 0 : ' + str.tostring(math.round_to_mintick(middle)) : i_calctype == 'Keltner Channel' ? 'KC 0 : ' + str.tostring(math.round_to_mintick(middle)) : i_calctype == 'Donchian Channel' ? 'DC 0 : ' + str.tostring(math.round_to_mintick(middle)) : na, yloc=yloc.price, color=color.new(i_michanclr, 100), textcolor=color.new(i_michanclr, 0), style=label.style_label_left, size=size.small)
    l2
    label.delete(l2[1])

if i_showbands and lowerstatefloat
    l3 = label.new(bar_index, i_calctype == 'Bollinger Bands' ? lower  : i_calctype ==  'Keltner Channel' ? lower  : i_calctype == 'Donchian Channel' ? lower  : na, i_calctype == 'Bollinger Bands' ? 'BB -1 : ' + str.tostring(math.round_to_mintick(lower)) : i_calctype == 'Keltner Channel' ? 'KC -1 : ' + str.tostring(math.round_to_mintick(lower)) : i_calctype == 'Donchian Channel' ? 'DC -1 : ' + str.tostring(math.round_to_mintick(lower)) : na, yloc=yloc.price, color=color.new(i_lochanclr, 100), textcolor=color.new(i_lochanclr, 0), style=label.style_label_left, size=size.small)
    l3
    label.delete(l3[1])

//◀─── Harmonic Patterns Calculation ───►

//Error Percentage Calculation

err_min = (100 - i_ratioprecision) / 100
err_max = (100 + i_ratioprecision) / 100

//Dynamic Length Function

f_dyn(bool para, float adaptiveperc, simple int minlen, simple int maxlen) =>
    var dyna_len         = int(na)
    var float dynamiclen = math.avg(minlen, maxlen)
    dynamiclen          := para ? math.max(minlen, dynamiclen * adaptiveperc) : math.min(maxlen, dynamiclen * (2 - adaptiveperc))
    dyna_len            := int(dynamiclen)
    dyna_len

//ZigZag Arguments Function

pivots_f(length) =>
    float phigh = ta.highestbars(upperstate ? i_uc ? close : high : upperstate, length) == 0 ? i_uc ? close : high : na
    float plow  = ta.lowestbars(lowerstate  ? i_uc ? close : low  : lowerstate, length) == 0 ? i_uc ? close : low  : na
    dir         = 0
    iff_1       = plow  and na(phigh) ? -1 : dir[1]
    dir        := phigh and na(plow)  ?  1 : iff_1
    [dir, phigh, plow]

//Pivots Drawing Definition Function

pivotsdir_f(length, pivots, pivotscount, pivotsdir) =>
    [dir, phigh, plow]     = pivots_f(length)
    dirchanged             = ta.change(dir)
    if phigh or plow
        value              = dir == 1 ? phigh : plow
        bar                = bar_index
        isnewdir           = dir
        if not dirchanged and array.size(pivots) >= 1
            pivot          = array.shift(pivots)
            pivotbar       = array.shift(pivotscount)
            pivotdir       = array.shift(pivotsdir)
            updatingvalues = value * pivotdir < pivot    * pivotdir
            value         := updatingvalues   ? pivot    : value
            bar           := updatingvalues   ? pivotbar : bar
            bar

        if array.size(pivots) >= 2
            lastpoint = array.get(pivots, 1)
            isnewdir := dir * value > dir * lastpoint ? dir * 2 : dir
            isnewdir
        array.unshift(pivots, value=value)
        array.unshift(pivotscount,    bar)
        array.unshift(pivotsdir, isnewdir)

        if array.size(pivots) > i_maxpvs
            array.pop(pivots)
            array.pop(pivotscount)
            array.pop(pivotsdir)

//Dynamic Length Variable Conditions

[dir, phigh, plow] = pivots_f(i_hpmaxlen)
up_para            = dir == 1
trendclr           = dir > 0 ? i_bullishclr : i_bearishclr
dynlength          = f_dyn(up_para, i_hpdynperc, i_hpminlen, i_hpmaxlen)

//Bar Color Plotting

barcolor(i_bc ? trendclr : na)

//ABCD Lines Drawing Definition Function

drawingabcd_f(a, b, c, d, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines) =>
    ab = line.new(y1=a, y2=b, x1=aleg, x2=bleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
    array.set(patternlines, 1, ab)
    bc = line.new(y1=b, y2=c, x1=bleg, x2=cleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
    array.set(patternlines, 2, bc)
    cd = line.new(y1=c, y2=d, x1=cleg, x2=dleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
    array.set(patternlines, 3, cd)

//XABCD Lines Drawing Definition Function

drawingxabcd_f(x, a, b, c, d, xleg, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines) =>
    xa = line.new(y1=x, y2=a, x1=xleg, x2=aleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
    array.set(patternlines, 0, xa)
    drawingabcd_f(a, b, c, d, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines)

//YXABCD Lines Drawing Definition Function

drawing_yxabcd_f(y, x, a, b, c, d, yleg, xleg, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines) =>
    drawingxabcd_f(x,  a, b, c, d,       xleg, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines)
    yx = line.new(y1=y, y2=x, x1=yleg, x2=xleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
    array.set(patternlines, 4, yx)

//ABCD Ratios Drawing Definition Function

drawingabcdratios_f(a, b, c, d, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio) =>
    bd        = line.new(y1=b, y2=d, x1=bleg, x2=dleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 1,       bd)
    ac        = line.new(y1=a, y2=c, x1=aleg, x2=cleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 3,       ac)
    bd_x      = math.abs(bleg + (dleg - bleg) / 2)
    bd_y      = math.abs(d    + (b    -    d) / 2)
    bd_string = str.tostring(bcdratio, '0.000')
    ratio_bd  = label.new(x=bd_x, y=bd_y, text=bd_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     1, ratio_bd)
    ac_x      = math.abs(aleg + (cleg - aleg) / 2)
    ac_y      = math.abs(c    + (a    -    c) / 2)
    ac_string = str.tostring(abcratio, '0.000')
    ratio_ac  = label.new(x=ac_x, y=ac_y, text=ac_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     3, ratio_ac)

//XABCD Ratios Drawing Definition Function

drawingxabcdratios_f(x, a, b, c, d, xleg, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio) =>
    xb        = line.new(y1=x, y2=b, x1=xleg, x2=bleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 0, xb)
    bd        = line.new(y1=b, y2=d, x1=bleg, x2=dleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 1, bd)
    xd        = line.new(y1=x, y2=d, x1=xleg, x2=dleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 2, xd)
    ac        = line.new(y1=a, y2=c, x1=aleg, x2=cleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 3,       ac)
    xb_x      = math.abs(xleg + (bleg - xleg) / 2)
    xb_y      = math.abs(x    + (b    -    x) / 2)
    xb_string = str.tostring(xabratio, '0.000')
    ratio_xb  = label.new(x=xb_x, y=xb_y, text=xb_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     0, ratio_xb)
    bd_x      = math.abs(bleg + (dleg - bleg) / 2)
    bd_y      = math.abs(d    + (b    -    d) / 2)
    bd_string = str.tostring(bcdratio, '0.000')
    ratio_bd  = label.new(x=bd_x, y=bd_y, text=bd_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     1, ratio_bd)
    xd_x      = math.abs(xleg + (dleg - xleg) / 2)
    xd_y      = math.abs(x    + (d    -    x) / 2)
    xd_string = str.tostring(xadratio, '0.000')
    ratio_xd  = label.new(x=xd_x, y=xd_y, text=xd_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     2, ratio_xd)
    ac_x      = math.abs(aleg + (cleg - aleg) / 2)
    ac_y      = math.abs(c    + (a    -    c) / 2)
    ac_string = str.tostring(abcratio, '0.000')
    ratio_ac  = label.new(x=ac_x, y=ac_y, text=ac_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     3, ratio_ac)

//YXABCD Ratio Drawing Definition Function

drawingyxabcdratios_f(y, x, a, b, c, d, yleg, xleg, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio) =>
    xb        = line.new(y1=x, y2=b, x1=xleg, x2=bleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 0,       xb)
    bd        = line.new(y1=b, y2=d, x1=bleg, x2=dleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 1,       bd)
    ac        = line.new(y1=a, y2=c, x1=aleg, x2=cleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 3,       ac)
    ya        = line.new(y1=y, y2=a, x1=yleg, x2=aleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
    array.set(ratiolines, 4,       ya)
    xb_x      = math.abs(xleg + (bleg - xleg) / 2)
    xb_y      = math.abs(x    + (b    -    x) / 2)
    xb_string = str.tostring(xabratio, '0.000')
    ratio_xb  = label.new(x=xb_x, y=xb_y, text=xb_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     0, ratio_xb)
    bd_x      = math.abs(bleg + (dleg - bleg) / 2)
    bd_y      = math.abs(d    + (b    -    d) / 2)
    bd_string = str.tostring(bcdratio, '0.000')
    ratio_bd  = label.new(x=bd_x, y=bd_y, text=bd_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     1, ratio_bd)
    ac_x      = math.abs(aleg + (cleg - aleg) / 2)
    ac_y      = math.abs(c    + (a    -    c) / 2)
    ac_string = str.tostring(abcratio, '0.000')
    ratio_ac  = label.new(x=ac_x, y=ac_y, text=ac_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     3, ratio_ac)
    ya_x      = math.abs(yleg + (aleg - yleg) / 2)
    ya_y      = math.abs(y    + (a    -    y) / 2)
    ya_string = str.tostring(yxaratio, '0.000')
    ratio_ya  = label.new(x=ya_x, y=ya_y, text=ya_string, textcolor=i_ratioclr, size=size.normal, style=label.style_none)
    array.set(ratios,     4, ratio_ya)

//Targets Drawing Definition Function

drawingtargets_f(c, d, dleg, i_stoploss, i_prz, i_target1, i_target2, i_target3, i_target4, targets, targetslabels, targetwidth) =>
    stoploss_y = math.abs(c + (d - c) * (1 - i_stoploss))
    prz_y      = math.abs(c + (d - c) * (1 -      i_prz))
    t1_y       = math.abs(c + (d - c) * (1 -  i_target1))
    t2_y       = math.abs(c + (d - c) * (1 -  i_target2))
    t3_y       = math.abs(c + (d - c) * (1 -  i_target3))
    t4_y       = math.abs(c + (d - c) * (1 -  i_target4))
    linesl     = line.new(y1=stoploss_y, y2=stoploss_y, x1=dleg, x2=dleg + targetwidth, color=i_stoplossclr, width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelsl    = label.new(x=dleg + targetwidth / 2, y=stoploss_y, text='Stop-Loss : ' + str.tostring(stoploss_y, format.mintick) + ' (' + str.tostring(i_stoploss * 100, '#.#') + ' %)', textcolor=i_stoplossclr, size=tleveladjustment, style=label.style_none)
    array.set(targets,       0,   linesl)
    array.set(targetslabels, 0,  labelsl)
    lineprz    = line.new(y1=prz_y,      y2=prz_y,      x1=dleg, x2=dleg + targetwidth, color=i_przclr,      width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelprz   = label.new(x=dleg + targetwidth / 2, y=prz_y,      text='PRZ : '       + str.tostring(prz_y,      format.mintick) + ' (' + str.tostring(i_prz      * 100, '#.#') + ' %)', textcolor=i_przclr,      size=tleveladjustment, style=label.style_none)
    array.set(targets,       1,  lineprz)
    array.set(targetslabels, 1, labelprz)
    linet1     = line.new(y1=t1_y,       y2=t1_y,       x1=dleg, x2=dleg + targetwidth, color=i_target1clr,  width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelt1    = label.new(x=dleg + targetwidth / 2, y=t1_y,       text='Target 1 : '  + str.tostring(t1_y,       format.mintick) + ' (' + str.tostring(i_target1  * 100, '#.#') + ' %)', textcolor=i_target1clr,  size=tleveladjustment, style=label.style_none)
    array.set(targets,       2,   linet1)
    array.set(targetslabels, 2,  labelt1)
    linet2     = line.new(y1=t2_y,       y2=t2_y,       x1=dleg, x2=dleg + targetwidth, color=i_target2clr,  width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelt2    = label.new(x=dleg + targetwidth / 2, y=t2_y,       text='Target 2 : '  + str.tostring(t2_y,       format.mintick) + ' (' + str.tostring(i_target2 * 100,  '#.#') + ' %)', textcolor=i_target2clr,  size=tleveladjustment, style=label.style_none)
    array.set(targets,       3,   linet2)
    array.set(targetslabels, 3,  labelt2)
    linet3     = line.new(y1=t3_y,       y2=t3_y,       x1=dleg, x2=dleg + targetwidth, color=i_target3clr,  width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelt3    = label.new(x=dleg + targetwidth / 2, y=t3_y,       text='Target 3 : '  + str.tostring(t3_y,       format.mintick) + ' (' + str.tostring(i_target3 * 100,  '#.#') + ' %)', textcolor=i_target3clr,  size=tleveladjustment, style=label.style_none)
    array.set(targets,       4,   linet3)
    array.set(targetslabels, 4,  labelt3)
    linet4     = line.new(y1=t4_y,       y2=t4_y,       x1=dleg, x2=dleg + targetwidth, color=i_target4clr, width=1, style=line.style_solid, extend=i_extendstargets ? extend.right : extend.none)
    labelt4    = label.new(x=dleg + targetwidth / 2, y=t4_y,       text='Target 4 : '  + str.tostring(t4_y,       format.mintick) + ' (' + str.tostring(i_target4 * 100,  '#.#') + ' %)', textcolor=i_target4clr,  size=tleveladjustment, style=label.style_none)
    array.set(targets,       5,   linet4)
    array.set(targetslabels, 5,  labelt4)

//Labels Drawing Arguments Definition Function

getlabels_f(patternlabels, dir, price, bar, drawhp) =>
    start                  = 1
    patterndetected        = false
    if array.size(pivots) >= 6 + start and drawhp
        d                  = array.get(pivots,                  start + 0)
        dleg               = array.get(pivotscount,             start + 0)
        dlegdir            = array.get(pivotsdir,               start + 0)
        c                  = array.get(pivots,                  start + 1)
        cleg               = array.get(pivotscount,             start + 1)
        clegdir            = array.get(pivotsdir,               start + 1)
        b                  = array.get(pivots,                  start + 2)
        bleg               = array.get(pivotscount,             start + 2)
        blegdir            = array.get(pivotsdir,               start + 2)
        a                  = array.get(pivots,                  start + 3)
        aleg               = array.get(pivotscount,             start + 3)
        alegdir            = array.get(pivotsdir,               start + 3)
        x                  = array.get(pivots,                  start + 4)
        xleg               = array.get(pivotscount,             start + 4)
        xlegdir            = array.get(pivotsdir,               start + 4)
        y                  = array.get(pivots,                  start + 5)
        yleg               = array.get(pivotscount,             start + 5)
        ylegdir            = array.get(pivotsdir,               start + 5)
        ratioduration      = math.abs(cleg - dleg) / math.abs(aleg - bleg)
        priceratio         = math.abs(c    -    d) / math.abs(a    -    b)
        xabratio           = math.abs(b    -    a) / math.abs(x    -    a)
        abcratio           = math.abs(c    -    b) / math.abs(a    -    b)
        bcdratio           = math.abs(d    -    c) / math.abs(b    -    c)
        xadratio           = math.abs(d    -    a) / math.abs(x    -    a)
        yxaratio           = math.abs(a    -    x) / math.abs(y    -    x)
        risk               = math.abs(b    -    d) / b * 100
        reward             = math.abs(c    -    d) / c * 100
        rpr                = risk * 100 / (risk + reward)
        pattern1           = array.get(patternlabels, 0)
        pattern2           = array.get(patternlabels, 1)
        pattern3           = array.get(patternlabels, 2)
        labeltext          = pattern1  ?                                 i_p1id : ''
        labeltext         += (pattern2 ? (labeltext == '' ? '' : '\n') + i_p2id : '')
        labeltext         += (pattern3 ? (labeltext == '' ? '' : '\n') + i_p3id : '')
        trendclr           = dir > 0   ? i_bullishclr : i_bearishclr

//Labels Tooltips Drawing Calculation

        labeltooltip = string(na)
        if labeltext == i_p1id
            if dir > 0
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip
            else
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip
        if labeltext == i_p2id
            if dir > 0
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip
            else
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip
        if labeltext == i_p3id
            if dir > 0
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip
            else
                labeltooltip := '                       - ROI Statistics - ' + '\n────────────────────' + '\n• Current Risk : ' + str.tostring(risk, format.percent) + '\n• Current Reward : ' + str.tostring(reward, format.percent) + '\n• Current Risk Per Reward : ' + str.tostring(rpr, format.percent) + '\n────────────────────' + '\n                    - XABCD Statistics - ' + '\n────────────────────' + '\n• XAB Ratio : ' + str.tostring(xabratio, '0.000') + '     • ABC Ratio : ' + str.tostring(abcratio, '0.000') + '\n• BCD Ratio : ' + str.tostring(bcdratio, '0.000') + '     • XAD Ratio : ' + str.tostring(xadratio, '0.000')
                labeltooltip

//Labels Plotting

        if dir > 0
            patlabel = label.new(x=bar, y=price, text=labeltext, yloc=yloc.price, color=trendclr, style=label.style_label_up,   textcolor=color.black, size=size.small, tooltip=labeltooltip)
            patlabel
        if dir < 0
            patlabel = label.new(x=bar, y=price, text=labeltext, yloc=yloc.price, color=trendclr, style=label.style_label_down, textcolor=color.black, size=size.small, tooltip=labeltooltip)
            patlabel

//Patterns Detection Calculation Function

patterndetection_f(pivots, pivotscount, pivotsdir, patternlines, patnewlabel, patterntype, patternlabels, leg, ratiolines, ratios, targets, targetslabels, drawhp) =>
    start                  = 1
    patterndetected        = false
    if array.size(pivots) >= 6 + start and drawhp
        d                  = array.get(pivots,                  start + 0)
        dleg               = array.get(pivotscount,             start + 0)
        dlegdir            = array.get(pivotsdir,               start + 0)
        c                  = array.get(pivots,                  start + 1)
        cleg               = array.get(pivotscount,             start + 1)
        clegdir            = array.get(pivotsdir,               start + 1)
        b                  = array.get(pivots,                  start + 2)
        bleg               = array.get(pivotscount,             start + 2)
        blegdir            = array.get(pivotsdir,               start + 2)
        a                  = array.get(pivots,                  start + 3)
        aleg               = array.get(pivotscount,             start + 3)
        alegdir            = array.get(pivotsdir,               start + 3)
        x                  = array.get(pivots,                  start + 4)
        xleg               = array.get(pivotscount,             start + 4)
        xlegdir            = array.get(pivotsdir,               start + 4)
        y                  = array.get(pivots,                  start + 5)
        yleg               = array.get(pivotscount,             start + 5)
        ylegdir            = array.get(pivotsdir,               start + 5)
        ratioduration      = math.abs(cleg - dleg) / math.abs(aleg - bleg)
        priceratio         = math.abs(c    -    d) / math.abs(a    -    b)
        xabratio           = math.abs(b    -    a) / math.abs(x    -    a)
        abcratio           = math.abs(c    -    b) / math.abs(a    -    b)
        bcdratio           = math.abs(d    -    c) / math.abs(b    -    c)
        xadratio           = math.abs(d    -    a) / math.abs(x    -    a)
        yxaratio           = math.abs(a    -    x) / math.abs(y    -    x)
        abcdlegdirection   = a   < b and a < c and c < b and c < d and a < d and b < d ? 1 : a > b and a > c and c > b and c > d and a > d and b > d ? -1 : 0
        dir                = c   > d ? 1            : -1
        trendclr           = dir > 0 ? i_bullishclr : i_bearishclr
        risk               = math.abs(b    -    d)
        reward             = math.abs(c    -    d)
        rpr                = risk * 100 / (risk + reward)
        highpoint          = math.max(x, a, b, c, d)
        lowpoint           = math.min(x, a, b, c, d)

//Pattern 1 Calculation

        if b < highpoint and b > lowpoint
            if i_pattern1 and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bullstate, 0, array.get(bearstate, 0) + 1)
                else
                    array.set(bearstate, 0, array.get(bearstate, 0) + 1)
            else
                array.set(patternlabels, 0, false)

//Pattern 2 Calculation

            if i_pattern2 and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bullstate, 1, array.get(bearstate, 1) + 1)
                else
                    array.set(bearstate, 1, array.get(bearstate, 1) + 1)
            else
                array.set(patternlabels, 1, false)

//Pattern 3 Calculation

            if i_pattern3 and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bullstate, 2, array.get(bearstate, 2) + 1)
                else
                    array.set(bearstate, 2, array.get(bearstate, 2) + 1)
            else
                array.set(patternlabels, 2, false)

//◀─── Backtesting Table ───►

//Pattern 1/Target 1 Variables Declaration

            var float startlongtrade  = open
            var float inlongtrade     = 0.
            var float startshorttrade = open
            var float inshorttrade    = 0.
            var int   totalexecuted   = 0
            var int   tradecounter    = 0

//Pattern 1/Target 1 Calculation

            if i_pattern1 and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bullstate, 0, array.get(bearstate, 0) + 1)
                startlongtrade  := math.abs(c +   (d - c) * (1 - i_prz))
                startlongtrade
            if i_pattern1 and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff            = math.abs(c +   (d - c) * (1 - i_target1))  - startlongtrade
                totalexecuted   := ldiff > 0 ? 1 : 0
                inlongtrade     := ldiff
                tradecounter    := 1
                tradecounter
            if i_pattern1 and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bearstate, 0, array.get(bearstate, 0) + 1)
                startshorttrade := math.abs(c +   (d - c) * (1 - i_prz))
                startshorttrade
            if i_pattern1 and  math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff            = startshorttrade - math.abs(c + (d - c) * (1 - i_target1))
                totalexecuted   := sdiff > 0 ? 1 : 0
                inshorttrade    := sdiff
                tradecounter    := 1
                tradecounter

//Pattern 1/Target 1 Conditions

            totaltrades         = ta.cum(tradecounter)
            totaltradesexecuted = ta.cum(totalexecuted)
            cumreturn           = totaltrades - totaltradesexecuted == 0 ? 1 : totaltrades - totaltradesexecuted

//Pattern 1/Target 2 Variables Declaration

            var float startlongtrade4  = open
            var float inlongtrade4     = 0.
            var float startshorttrade4 = open
            var float inshorttrade4    = 0.
            var int   totalexecuted4   = 0
            var int   tradecounter4    = 0

//Pattern 1/Target 2 Calculation

            if i_pattern1    and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected  := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bullstate, 0, array.get(bearstate, 0) + 1)
                startlongtrade4  := math.abs(c  + (d - c) * (1 - i_prz))
                startlongtrade4
            if i_pattern1    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff4            = math.abs(c  + (d - c) * (1 - i_target2))     - startlongtrade4
                totalexecuted4   := ldiff4 > 0 ? 1 : 0
                inlongtrade4     := ldiff4
                tradecounter4    := 1
                tradecounter4
            if i_pattern1    and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected  := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bearstate, 0, array.get(bearstate, 0) + 1)
                startshorttrade4 := math.abs(c  + (d - c) * (1 - i_prz))
                startshorttrade4
            if i_pattern1    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff4            = startshorttrade4 - math.abs(c + (d - c) * (1 - i_target2))
                totalexecuted4   := sdiff4 > 0 ? 1 : 0
                inshorttrade4    := sdiff4
                tradecounter4    := 1
                tradecounter4

//Pattern 1/Target 2 Conditions

            totaltrades4         = ta.cum(tradecounter4)
            totaltradesexecuted4 = ta.cum(totalexecuted4)
            cumreturn4           = totaltrades4 - totaltradesexecuted4 == 0 ? 1 : totaltrades4 - totaltradesexecuted4

//Pattern 1/Target 3 Variables Declaration

            var float startlongtrade7  = open
            var float inlongtrade7     = 0.
            var float startshorttrade7 = open
            var float inshorttrade7    = 0.
            var int   totalexecuted7   = 0
            var int   tradecounter7    = 0

//Pattern 1/Target 3 Calculation

            if i_pattern1    and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected  := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bullstate, 0, array.get(bearstate, 0) + 1)
                startlongtrade7  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade7
            if i_pattern1    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff7            = math.abs(c +  (d - c) * (1 - i_target3))     - startlongtrade7
                totalexecuted7   := ldiff7 > 0 ? 1 : 0
                inlongtrade7     := ldiff7
                tradecounter7    := 1
                tradecounter7
            if i_pattern1    and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected  := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bearstate, 0, array.get(bearstate, 0) + 1)
                startshorttrade7 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade7
            if i_pattern1    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff7            = startshorttrade7 - math.abs(c + (d - c) * (1 - i_target3))
                totalexecuted7   := sdiff7 > 0 ? 1 : 0
                inshorttrade7    := sdiff7
                tradecounter7    := 1
                tradecounter7

//Pattern 1/Target 3 Conditions

            totaltrades7         = ta.cum(tradecounter7)
            totaltradesexecuted7 = ta.cum(totalexecuted7)
            cumreturn7           = totaltrades7 - totaltradesexecuted7 == 0 ? 1 : totaltrades7 - totaltradesexecuted7

//Pattern 1/Target 4 Variables Declaration

            var float startlongtrade10  = open
            var float inlongtrade10     = 0.
            var float startshorttrade10 = open
            var float inshorttrade10    = 0.
            var int   totalexecuted10   = 0
            var int   tradecounter10    = 0

//Pattern 1/Target 4 Calculation

            if i_pattern1      and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected   := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bullstate, 0, array.get(bearstate, 0) + 1)
                startlongtrade10  := math.abs(c + (d - c) * (1 - i_prz))
                startlongtrade10
            if i_pattern1      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff10            = math.abs(c + (d - c) * (1 - i_target4))       - startlongtrade10
                totalexecuted10   := ldiff10 > 0 ? 1 : 0
                inlongtrade10     := ldiff10
                tradecounter10    := 1
                tradecounter10
            if i_pattern1      and xabratio >= i_bullpattern1min * err_min and xabratio <= i_bullpattern1max * err_max and abcratio >= i_bearpattern1min * err_min and abcratio <= i_bearpattern1max * err_max
                patterndetected   := true
                array.set(patternlabels, 0, true)
                if dir > 0
                    array.set(bearstate, 0, array.get(bearstate, 0) + 1)
                startshorttrade10 := math.abs(c + (d - c) * (1 - i_prz))
                startshorttrade10
            if i_pattern1      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff10            = startshorttrade10 - math.abs(c + (d - c) * (1 - i_target4))
                totalexecuted10   := sdiff10 > 0 ? 1 : 0
                inshorttrade10    := sdiff10
                tradecounter10    := 1
                tradecounter10

//Pattern 1/Target 4 Conditions

            totaltrades10         = ta.cum(tradecounter10)
            totaltradesexecuted10 = ta.cum(totalexecuted10)
            cumreturn10           = totaltrades10 - totaltradesexecuted10 == 0 ? 1 : totaltrades10 - totaltradesexecuted10

//Pattern 2/Target 1 Variables Declaration

            var float startlongtrade2  = open
            var float inlongtrade2     = 0.
            var float startshorttrade2 = open
            var float inshorttrade2    = 0.
            var int   totalexecuted2   = 0
            var int   tradecounter2    = 0

//Pattern 2/Target 1 Calculation

            if i_pattern2    and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bullstate, 1, array.get(bearstate, 1) + 1)
                startlongtrade2  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade2
            if i_pattern2    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff2            = math.abs(c +  (d - c) * (1 - i_target1))     - startlongtrade2
                totalexecuted2   := ldiff2 > 0 ? 1 : 0
                inlongtrade2     := ldiff2
                tradecounter2    := 1
                tradecounter2
            if i_pattern2    and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bearstate, 1, array.get(bearstate, 1) + 1)
                startshorttrade2 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade2
            if i_pattern2    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff2            = startshorttrade2 - math.abs(c + (d - c) * (1 - i_target1))
                totalexecuted2   := sdiff2 > 0 ? 1 : 0
                inshorttrade2    := sdiff2
                tradecounter2    := 1
                tradecounter2

//Pattern 2/Target 1 Conditions

            totaltrades2         = ta.cum(tradecounter2)
            totaltradesexecuted2 = ta.cum(totalexecuted2)
            cumreturn2           = totaltrades2 - totaltradesexecuted2 == 0 ? 1 : totaltrades2 - totaltradesexecuted2

//Pattern 2/Target 2 Variables Declaration

            var float startlongtrade5  = open
            var float inlongtrade5     = 0.
            var float startshorttrade5 = open
            var float inshorttrade5    = 0.
            var int   totalexecuted5   = 0
            var int   tradecounter5    = 0

//Pattern 2/Target 2 Calculation

            if i_pattern2   and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bullstate, 1, array.get(bearstate, 1) + 1)
                startlongtrade5  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade5
            if i_pattern2   and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff5            = math.abs(c +  (d - c) * (1 - i_target2))    - startlongtrade5
                totalexecuted5   := ldiff5 > 0 ? 1 : 0
                inlongtrade5     := ldiff5
                tradecounter5    := 1
                tradecounter5
            if i_pattern2   and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bearstate, 1, array.get(bearstate, 1) + 1)
                startshorttrade5 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade5
            if i_pattern2    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff5            = startshorttrade5 - math.abs(c + (d - c) * (1 - i_target2))
                totalexecuted5   := sdiff5 > 0 ? 1 : 0
                inshorttrade5    := sdiff5
                tradecounter5    := 1
                tradecounter5

//Pattern 2/Target 2 Conditions

            totaltrades5         = ta.cum(tradecounter5)
            totaltradesexecuted5 = ta.cum(totalexecuted5)
            cumreturn5           = totaltrades5 - totaltradesexecuted5 == 0 ? 1 : totaltrades5 - totaltradesexecuted5

//Pattern 2/Target 3 Variables Declaration

            var float startlongtrade8  = open
            var float inlongtrade8     = 0.
            var float startshorttrade8 = open
            var float inshorttrade8    = 0.
            var int   totalexecuted8   = 0
            var int   tradecounter8    = 0

//Pattern 2/Target 3 Calculation

            if i_pattern2    and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bullstate, 1, array.get(bearstate, 1) + 1)
                startlongtrade8  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade8
            if i_pattern2    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff8            = math.abs(c +  (d - c) * (1 - i_target3))     - startlongtrade8
                totalexecuted8   := ldiff8 > 0 ? 1 : 0
                inlongtrade8     := ldiff8
                tradecounter8    := 1
                tradecounter8
            if i_pattern2    and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected  := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bearstate, 1, array.get(bearstate, 1) + 1)
                startshorttrade8 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade8
            if i_pattern2    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff8            = startshorttrade8 - math.abs(c + (d - c) * (1 - i_target3))
                totalexecuted8   := sdiff8 > 0 ? 1 : 0
                inshorttrade8    := sdiff8
                tradecounter8    := 1
                tradecounter8

//Pattern 2/Target 3 Conditions

            totaltrades8         = ta.cum(tradecounter8)
            totaltradesexecuted8 = ta.cum(totalexecuted8)
            cumreturn8           = totaltrades8 - totaltradesexecuted8 == 0 ? 1 : totaltrades8 - totaltradesexecuted8

//Pattern 2/Target 4 Variables Declaration

            var float startlongtrade11  = open
            var float inlongtrade11     = 0.
            var float startshorttrade11 = open
            var float inshorttrade11    = 0.
            var int   totalexecuted11   = 0
            var int   tradecounter11    = 0

//Pattern 2/Target 4 Calculation

            if i_pattern2      and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected   := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bullstate, 1, array.get(bearstate, 1) + 1)
                startlongtrade11  := math.abs(c + (d - c) * (1 - i_prz))
                startlongtrade11
            if i_pattern2      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff11            = math.abs(c + (d - c) * (1 - i_target4))       - startlongtrade11
                totalexecuted11   := ldiff11 > 0 ? 1 : 0
                inlongtrade11     := ldiff11
                tradecounter11    := 1
                tradecounter11
            if i_pattern2      and xabratio >= i_bullpattern2min * err_min and xabratio <= i_bullpattern2max * err_max and abcratio >= i_bearpattern2min * err_min and abcratio <= i_bearpattern2max * err_max
                patterndetected   := true
                array.set(patternlabels, 1, true)
                if dir > 0
                    array.set(bearstate, 1, array.get(bearstate, 1) + 1)
                startshorttrade11 := math.abs(c + (d - c) * (1 - i_prz))
                startshorttrade11
            if i_pattern2      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff11            = startshorttrade11 - math.abs(c + (d - c) * (1 - i_target4))
                totalexecuted11   := sdiff11 > 0 ? 1 : 0
                inshorttrade11    := sdiff11
                tradecounter11    := 1
                tradecounter11

//Pattern 2/Target 4 Conditions

            totaltrades11         = ta.cum(tradecounter11)
            totaltradesexecuted11 = ta.cum(totalexecuted11)
            cumreturn11           = totaltrades11 - totaltradesexecuted11 == 0 ? 1 : totaltrades11 - totaltradesexecuted11

//Pattern 3/Target 1 Variables Declaration

            var float startlongtrade3  = open
            var float inlongtrade3     = 0.
            var float startshorttrade3 = open
            var float inshorttrade3    = 0.
            var int   totalexecuted3   = 0
            var int   tradecounter3    = 0

//Pattern 3/Target 1 Calculation

            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bullstate, 2, array.get(bearstate, 2) + 1)
                startlongtrade3  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade3
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff3            = math.abs(c +  (d - c) * (1 - i_target1))     - startlongtrade3
                totalexecuted3   := ldiff3 > 0 ? 1 : 0
                inlongtrade3     := ldiff3
                tradecounter3    := 1
                tradecounter3
            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bearstate, 2, array.get(bearstate, 2) + 1)
                startshorttrade3 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade3
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target1)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff3            = startshorttrade3 - math.abs(c + (d - c) * (1 - i_target1))
                totalexecuted3   := sdiff3 > 0 ? 1 : 0
                inshorttrade3    := sdiff3
                tradecounter3    := 1
                tradecounter3

//Pattern 3/Target 1 Conditions

            totaltrades3         = ta.cum(tradecounter3)
            totaltradesexecuted3 = ta.cum(totalexecuted3)
            cumreturn3           = totaltrades3 - totaltradesexecuted3 == 0 ? 1 : totaltrades3 - totaltradesexecuted3

//Pattern 3/Target 2 Variables Declaration

            var float startlongtrade6  = open
            var float inlongtrade6     = 0.
            var float startshorttrade6 = open
            var float inshorttrade6    = 0.
            var int   totalexecuted6   = 0
            var int   tradecounter6    = 0

//Pattern 3/Target 2 Calculation

            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bullstate, 2, array.get(bearstate, 2) + 1)
                startlongtrade6  := math.abs(c +  (d - c) * (1 - i_prz))
                startlongtrade6
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff6            = math.abs(c +  (d - c) * (1 - i_target2))     - startlongtrade6
                totalexecuted6   := ldiff6 > 0 ? 1 : 0
                inlongtrade6     := ldiff6
                tradecounter6    := 1
                tradecounter6
            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bearstate, 2, array.get(bearstate, 2) + 1)
                startshorttrade6 := math.abs(c +  (d - c) * (1 - i_prz))
                startshorttrade6
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target2)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff6            = startshorttrade6 - math.abs(c + (d - c) * (1 - i_target2))
                totalexecuted6   := sdiff6 > 0 ? 1 : 0
                inshorttrade6    := sdiff6
                tradecounter6    := 1
                tradecounter6

//Pattern 3/Target 2 Conditions

            totaltrades6         = ta.cum(tradecounter6)
            totaltradesexecuted6 = ta.cum(totalexecuted6)
            cumreturn6           = totaltrades6 - totaltradesexecuted6 == 0 ? 1 : totaltrades6 - totaltradesexecuted6

//Pattern 3/Target 3 Variables Declaration

            var float startlongtrade9  = open
            var float inlongtrade9     = 0.
            var float startshorttrade9 = open
            var float inshorttrade9    = 0.
            var int   totalexecuted9   = 0
            var int   tradecounter9    = 0

//Pattern 3/Target 3 Calculation

            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bullstate, 2, array.get(bearstate, 2) + 1)
                startlongtrade9  := math.abs(c  + (d - c) * (1 - i_prz))
                startlongtrade9
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff9            = math.abs(c  + (d - c) * (1 - i_target3))     - startlongtrade9
                totalexecuted9   := ldiff9 > 0 ? 1 : 0
                inlongtrade9     := ldiff9
                tradecounter9    := 1
                tradecounter9
            if i_pattern3    and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected  := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bearstate, 2, array.get(bearstate, 2) + 1)
                startshorttrade9 := math.abs(c  + (d - c) * (1 - i_prz))
                startshorttrade9
            if i_pattern3    and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target3)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff9            = startshorttrade9 - math.abs(c + (d - c) * (1 - i_target3))
                totalexecuted9   := sdiff9 > 0 ? 1 : 0
                inshorttrade9    := sdiff9
                tradecounter9    := 1
                tradecounter9

//Pattern 3/Target 3 Conditions

            totaltrades9         = ta.cum(tradecounter9)
            totaltradesexecuted9 = ta.cum(totalexecuted9)
            cumreturn9           = totaltrades9 - totaltradesexecuted9 == 0 ? 1 : totaltrades9 - totaltradesexecuted9

//Pattern 3/Target 4 Variables Declaration

            var float startlongtrade12  = open
            var float inlongtrade12     = 0.
            var float startshorttrade12 = open
            var float inshorttrade12    = 0.
            var int   totalexecuted12   = 0
            var int   tradecounter12    = 0

//Pattern 3/Target 4 Calculation

            if i_pattern3      and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected   := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bullstate, 2, array.get(bearstate, 2) + 1)
                startlongtrade12  := math.abs(c + (d - c) * (1 - i_prz))
                startlongtrade12
            if i_pattern3      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * xabratio * (dir == 1 ? -1 : 1))
                ldiff12            = math.abs(c + (d - c) * (1 - i_target4))       - startlongtrade12
                totalexecuted12   := ldiff12 > 0 ? 1 : 0
                inlongtrade12     := ldiff12
                tradecounter12    := 1
                tradecounter12
            if i_pattern3      and xabratio >= i_bullpattern3min * err_min and xabratio <= i_bullpattern3max * err_max and abcratio >= i_bearpattern3min * err_min and abcratio <= i_bearpattern3max * err_max
                patterndetected   := true
                array.set(patternlabels, 2, true)
                if dir > 0
                    array.set(bearstate, 2, array.get(bearstate, 2) + 1)
                startshorttrade12 := math.abs(c + (d - c) * (1 - i_prz))
                startshorttrade12
            if i_pattern3      and math.round_to_mintick(math.abs(c + (d - c) * (1 - i_target4)) * abcratio * (dir == 1 ? -1 : 1))
                sdiff12            = startshorttrade12 - math.abs(c + (d - c) * (1 - i_target4))
                totalexecuted12   := sdiff12 > 0 ? 1 : 0
                inshorttrade12    := sdiff12
                tradecounter12    := 1
                tradecounter12

//Pattern 3/Target 4 Conditions

            totaltrades12         = ta.cum(tradecounter12)
            totaltradesexecuted12 = ta.cum(totalexecuted12)
            cumreturn12           = totaltrades12 - totaltradesexecuted12 == 0 ? 1 : totaltrades12 - totaltradesexecuted12

//Total Trades Calculation

            tt1               = (totaltradesexecuted  + totaltradesexecuted4 + totaltradesexecuted7 + totaltradesexecuted10) / 4
            tt2               = (totaltradesexecuted2 + totaltradesexecuted5 + totaltradesexecuted8 + totaltradesexecuted11) / 4
            tt3               = (totaltradesexecuted3 + totaltradesexecuted6 + totaltradesexecuted9 + totaltradesexecuted12) / 4
            totaltradesreturn = (tt1 + tt2 + tt3)

//Total Returns Calculation

            totalreturn1 = (totaltradesexecuted   * 100 / (totaltradesexecuted   + cumreturn)   + (totaltradesexecuted2  * 100 / (totaltradesexecuted2  + cumreturn2)  + (totaltradesexecuted3  * 100 / (totaltradesexecuted3  + cumreturn3))))  / 3
            totalreturn2 = (totaltradesexecuted4  * 100 / (totaltradesexecuted4  + cumreturn4)  + (totaltradesexecuted5  * 100 / (totaltradesexecuted5  + cumreturn5)  + (totaltradesexecuted6  * 100 / (totaltradesexecuted6  + cumreturn6))))  / 3
            totalreturn3 = (totaltradesexecuted7  * 100 / (totaltradesexecuted7  + cumreturn7)  + (totaltradesexecuted8  * 100 / (totaltradesexecuted8  + cumreturn8)  + (totaltradesexecuted9  * 100 / (totaltradesexecuted9  + cumreturn9))))  / 3
            totalreturn4 = (totaltradesexecuted10 * 100 / (totaltradesexecuted10 + cumreturn10) + (totaltradesexecuted11 * 100 / (totaltradesexecuted11 + cumreturn11) + (totaltradesexecuted12 * 100 / (totaltradesexecuted12 + cumreturn12)))) / 3

//Table Variables Declaration

            ssltable     = table.new(tablepos, 6, 30, bgcolor=color.new(color.black, 0), border_color=color.new(#000000, 0), border_width=2)
            i_showtables = true

//String Calculation

            if i_showtable and barstate.islast or i_showtable and barstate.ishistory
                if i_showtables
                    string _txt_pat1_tt1 = str.tostring(tt1,                                                                            '#')
                    string _txt_pat2_tt2 = str.tostring(tt2,                                                                            '#')
                    string _txt_pat3_tt3 = str.tostring(totaltradesexecuted3,                                                           '#')
                    string _txt_patt_tt  = str.tostring(totaltradesreturn,                                                              '#')
                    string _txt_pat1_t1  = str.tostring(totaltradesexecuted   * 100 / (totaltradesexecuted   +  cumreturn),  format.percent)
                    string _txt_pat2_t1  = str.tostring(totaltradesexecuted2  * 100 / (totaltradesexecuted2  +  cumreturn2), format.percent)
                    string _txt_pat3_t1  = str.tostring(totaltradesexecuted3  * 100 / (totaltradesexecuted3  +  cumreturn3), format.percent)
                    string _txt_total_t1 = str.tostring(totalreturn1,                                                        format.percent)
                    string _txt_pat1_t2  = str.tostring(totaltradesexecuted4  * 100 / (totaltradesexecuted4  +  cumreturn4), format.percent)
                    string _txt_pat2_t2  = str.tostring(totaltradesexecuted5  * 100 / (totaltradesexecuted5  +  cumreturn5), format.percent)
                    string _txt_pat3_t2  = str.tostring(totaltradesexecuted6  * 100 / (totaltradesexecuted6  +  cumreturn6), format.percent)
                    string _txt_total_t2 = str.tostring(totalreturn2,                                                        format.percent)
                    string _txt_pat1_t3  = str.tostring(totaltradesexecuted7  * 100 / (totaltradesexecuted7  +  cumreturn7), format.percent)
                    string _txt_pat2_t3  = str.tostring(totaltradesexecuted8  * 100 / (totaltradesexecuted8  +  cumreturn8), format.percent)
                    string _txt_pat3_t3  = str.tostring(totaltradesexecuted9  * 100 / (totaltradesexecuted9  +  cumreturn9), format.percent)
                    string _txt_total_t3 = str.tostring(totalreturn3,                                                        format.percent)
                    string _txt_pat1_t4  = str.tostring(totaltradesexecuted10 * 100 / (totaltradesexecuted10 + cumreturn10), format.percent)
                    string _txt_pat2_t4  = str.tostring(totaltradesexecuted11 * 100 / (totaltradesexecuted11 + cumreturn11), format.percent)
                    string _txt_pat3_t4  = str.tostring(totaltradesexecuted12 * 100 / (totaltradesexecuted12 + cumreturn12), format.percent)
                    string _txt_total_t4 = str.tostring(totalreturn4,                                                        format.percent)

//Columns/Rows Calculation

                    table.cell(ssltable, 0, 0, text='Patterns',    text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 0, 1, text=i_p1id,        text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 0, 2, text=i_p2id,        text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 0, 3, text=i_p3id,        text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 0, 4, text='Total',       text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 1, 0, text='Trades',      text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 1, 1, text=_txt_pat1_tt1, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 1, 2, text=_txt_pat2_tt2, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 1, 3, text=_txt_pat3_tt3, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 1, 4, text=_txt_patt_tt,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 2, 0, text='T1 [%]',      text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 2, 1, text=_txt_pat1_t1,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 2, 2, text=_txt_pat2_t1,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 2, 3, text=_txt_pat3_t1,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 2, 4, text=_txt_total_t1, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 3, 0, text='T2 [%]',      text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 3, 1, text=_txt_pat1_t2,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 3, 2, text=_txt_pat2_t2,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 3, 3, text=_txt_pat3_t2,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 3, 4, text=_txt_total_t2, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 4, 0, text='T3 [%]',      text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 4, 1, text=_txt_pat1_t3,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 4, 2, text=_txt_pat2_t3,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 4, 3, text=_txt_pat3_t3,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 4, 4, text=_txt_total_t3, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 5, 0, text='T4 [%]',      text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(#000000,     0))
                    table.cell(ssltable, 5, 1, text=_txt_pat1_t4,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 5, 2, text=_txt_pat2_t4,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 5, 3, text=_txt_pat3_t4,  text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))
                    table.cell(ssltable, 5, 4, text=_txt_total_t4, text_color=color.new(color.white, 0), text_size=size.small, bgcolor=color.new(color.black, 0))

//◀─── Harmonic Patterns Drawing ───►

        if patterndetected[1] and b == b[1]
            label.delete(array.get(patnewlabel,       0))
            line.delete(array.get(patternlines,       5))
            label.delete(array.get(leg,               2))
            label.delete(array.get(leg,               4))
        if patterndetected[1] and a == a[1] and b == b[1] and c == c[1]
            label.delete(array.get(patnewlabel,       0))
            for i = 1 to 3 by 1
                line.delete(array.get(patternlines,   i))
            for i = 1 to 4 by 1
                label.delete(array.get(leg,           i))
            line.delete(array.get(ratiolines,         1))
            line.delete(array.get(ratiolines,         3))
            label.delete(array.get(ratios,            1))
            label.delete(array.get(ratios,            3))
            for i = 0 to 5 by 1
                line.delete(array.get(targets,        i))
            for i = 0 to 5 by 1
                label.delete(array.get(targetslabels, i))
        if patterndetected[1] and a == a[1] and b == b[1] and c == c[1]
            label.delete(array.get(patnewlabel,       0))
            for i = 0 to 3 by 1
                line.delete(array.get(patternlines,   i))
            for i = 0 to 4 by 1
                label.delete(array.get(leg,           i))
            for i = 0 to 3 by 1
                line.delete(array.get(ratiolines,     i))
            for i = 0 to 3 by 1
                label.delete(array.get(ratios,        i))
            for i = 0 to 5 by 1
                line.delete(array.get(targets,        i))
            for i = 0 to 5 by 1
                label.delete(array.get(targetslabels, i))

//XABCD Patterns/Projections Drawing Calculation

        if patterndetected
            array.set(patterntype, 0, dir)
            if i_pattern1        == true
                float xd_ycalc = 0.0000
                if x < a
                    xd_ycalc  := math.abs(x + x * i_pattern1projbdratio / 100)
                if x > a
                    xd_ycalc  := math.abs(x - x * i_pattern1projcdratio / 100)
                xa             = line.new(y1=x, y2=a, x1=xleg, x2=aleg, color=trendclr,   width=i_hpwidth,         style=patternlinestyle)
                array.set(patternlines, 0, xa)
                xb             = line.new(y1=x, y2=b, x1=xleg, x2=bleg, color=i_ratioclr, width=i_ratiolineswidth, style=ratiolinestyle)
                array.set(patternlines, 0, xb)
                ab             = line.new(y1=a, y2=b, x1=aleg, x2=bleg, color=trendclr,   width=i_hpwidth,         style=patternlinestyle)
                array.set(patternlines, 1, ab)
                bc             = line.new(y1=b, y2=c, x1=bleg, x2=cleg, color=trendclr,   width=i_hpwidth,         style=patternlinestyle)
                array.set(patternlines, 2, bc)
                bd             = i_showprojections ? line.new(y1=b,        y2=xd_ycalc, x1=bleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_ratiolineswidth, style=line.style_dashed) : na
                array.set(patternlines, 1, bd)
                cd             = i_showprojections ? line.new(y1=c,        y2=xd_ycalc, x1=cleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_hpwidth,         style=line.style_dashed) : na
                array.set(patternlines, 3, cd)
                cdp            = i_showprojections ? line.new(y1=xd_ycalc, y2=xd_ycalc, x1=dleg, x2=dleg + 100, color=trendclr,                width=1,                 style=line.style_dotted, extend=i_extendprojections ? extend.right : extend.none) : na
                cdplabel       = i_showprojections ? label.new(x=dleg + 50, y=xd_ycalc, text='BD Projection Leg : ' + str.tostring(xd_ycalc, format.mintick), textcolor=trendclr, size=tleveladjustment, style=label.style_none) : na
                linefill.new(xa, ab, color.new(trendclr, i_bgfilling))
                linefill.new(xb, ab, color.new(trendclr, i_bgfilling))
                linefill.new(bc, cd, color.new(trendclr, i_bgfilling))
                linefill.new(bc, bd, color.new(trendclr, i_bgfilling))
            if i_pattern2        == true
                float xd_ycalc = 0.0000
                if x < a
                    xd_ycalc  := math.abs(x - x * i_pattern2projbdratio / 100)
                if x > a
                    xd_ycalc  := math.abs(x + x * i_pattern2projcdratio / 100)
                xa             = line.new(y1=x, y2=a, x1=xleg, x2=aleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 0, xa)
                xb             = line.new(y1=x, y2=b, x1=xleg, x2=bleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 0, xb)
                ab             = line.new(y1=a, y2=b, x1=aleg, x2=bleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 1, ab)
                bc             = line.new(y1=b, y2=c, x1=bleg, x2=cleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 2, bc)
                bd             = i_showprojections ? line.new(y1=b,        y2=xd_ycalc, x1=bleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_ratiolineswidth, style=line.style_dashed) : na
                array.set(patternlines, 1, bd)
                cd             = i_showprojections ? line.new(y1=c,        y2=xd_ycalc, x1=cleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_hpwidth,         style=line.style_dashed) : na
                array.set(patternlines, 3, cd)
                cdp            = i_showprojections ? line.new(y1=xd_ycalc, y2=xd_ycalc, x1=dleg, x2=dleg + 100, color=trendclr, width=1, style=line.style_dotted, extend=i_extendprojections ? extend.right : extend.none) : na
                cdplabel       = i_showprojections ? label.new(x=dleg + 50, y=xd_ycalc, text='CD Projection Leg : ' + str.tostring(xd_ycalc, format.mintick), textcolor=trendclr, size=tleveladjustment, style=label.style_none) : na
                linefill.new(xa, ab, color.new(trendclr, i_bgfilling))
                linefill.new(xb, ab, color.new(trendclr, i_bgfilling))
                linefill.new(bc, cd, color.new(trendclr, i_bgfilling))
                linefill.new(bc, bd, color.new(trendclr, i_bgfilling))
            if i_pattern3        == true
                float xd_ycalc = 0.0000
                if x < a
                    xd_ycalc  := math.abs(x + x * i_pattern3projbdratio / 100)
                if x > a
                    xd_ycalc  := math.abs(x - x * i_pattern3projcdratio / 100)
                xa             = line.new(y1=x, y2=a, x1=xleg, x2=aleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 0, xa)
                xb             = line.new(y1=x, y2=b, x1=xleg, x2=bleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 0, xb)
                ab             = line.new(y1=a, y2=b, x1=aleg, x2=bleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 1, ab)
                bc             = line.new(y1=b, y2=c, x1=bleg, x2=cleg, color=trendclr, width=i_hpwidth, style=patternlinestyle)
                array.set(patternlines, 2, bc)
                bd             = i_showprojections ? line.new(y1=b,        y2=xd_ycalc, x1=bleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_ratiolineswidth, style=line.style_dashed) : na
                array.set(patternlines, 1, bd)
                cd             = i_showprojections ? line.new(y1=c,        y2=xd_ycalc, x1=cleg, x2=dleg + 100, color=color.new(trendclr, 35), width=i_hpwidth,         style=line.style_dashed) : na
                array.set(patternlines, 3, cd)
                cdp            = i_showprojections ? line.new(y1=xd_ycalc, y2=xd_ycalc, x1=dleg, x2=dleg + 100, color=trendclr, width=1, style=line.style_dotted, extend=i_extendprojections ? extend.right : extend.none) : na
                cdplabel       = i_showprojections ? label.new(x=dleg + 50, y=xd_ycalc, text='BD Projection Leg : ' + str.tostring(xd_ycalc, format.mintick), textcolor=trendclr, size=tleveladjustment, style=label.style_none) : na
                linefill.new(xa, ab, color.new(trendclr, i_bgfilling))
                linefill.new(xb, ab, color.new(trendclr, i_bgfilling))
                linefill.new(bc, cd, color.new(trendclr, i_bgfilling))
                linefill.new(bc, bd, color.new(trendclr, i_bgfilling))
                if i_ratioslines == true
                    drawingxabcdratios_f(x, a, b, c, d, xleg, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio)
                if i_showtargets == true
                    drawingtargets_f(c, d, dleg, i_stoploss, i_prz, i_target1, i_target2, i_target3, i_target4, targets, targetslabels, 100)

//Legs/Ratios Drawing Calculation

            if dir > 0
                drawing_yxabcd_f(y, x, a, b, c, d, yleg, xleg, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines)
                if i_ratioslabels == true
                    point_y = label.new(x=yleg, y=y + math.abs((b - c) * 0.1), text='Y', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 5, point_y)
                    point_x = label.new(x=xleg, y=x - math.abs((b - c) * 0.2), text='X', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 0, point_x)
                    point_a = label.new(x=aleg, y=a + math.abs((b - c) * 0.1), text='A', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 1, point_a)
                    point_b = label.new(x=bleg, y=b - math.abs((b - c) * 0.2), text='B', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 2, point_b)
                    point_c = label.new(x=cleg, y=c + math.abs((b - c) * 0.1), text='C', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 3, point_c)
                    point_d = label.new(x=dleg, y=d - math.abs((b - c) * 0.2), text='D', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 4, point_d)
                if i_ratioslines  == true
                    drawingyxabcdratios_f(y, x, a, b, c, d, yleg, xleg, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio)
                if i_showtargets  == true
                    drawingtargets_f(c, d, dleg, i_stoploss, i_prz, i_target1, i_target2, i_target3, i_target4, targets, targetslabels, 100)

            if dir < 0
                drawingxabcd_f(x, a, b, c, d, xleg, aleg, bleg, cleg, dleg, trendclr, i_hpwidth, patternlinestyle, patternlines)
                if i_ratioslabels == true
                    point_x = label.new(x=xleg, y=x + math.abs((b - c) * 0.1), text='X', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    point_a = label.new(x=aleg, y=a - math.abs((b - c) * 0.2), text='A', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    point_b = label.new(x=bleg, y=b + math.abs((b - c) * 0.1), text='B', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    point_c = label.new(x=cleg, y=c - math.abs((b - c) * 0.2), text='C', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    point_d = label.new(x=dleg, y=d + math.abs((b - c) * 0.1), text='D', textcolor=i_ratioslabelsclr, size=lpatternadjustment, style=label.style_none)
                    array.set(leg, 0, point_x)
                    array.set(leg, 1, point_a)
                    array.set(leg, 2, point_b)
                    array.set(leg, 3, point_c)
                    array.set(leg, 4, point_d)
                if i_ratioslines  == true
                    drawingxabcdratios_f(x, a, b, c, d, xleg, aleg, bleg, cleg, dleg, i_ratioclr, i_ratiolineswidth, ratiolinestyle, ratiolines, ratios, xabratio, abcratio, bcdratio, xadratio, yxaratio)
                if i_showtargets  == true
                    drawingtargets_f(c, d, dleg, i_stoploss, i_prz, i_target1, i_target2, i_target3, i_target4, targets, targetslabels, 100)

//Pattern Drawing Definition

        if patterndetected
            array.set(patnewlabel, 0, getlabels_f(patternlabels, dir, d, dleg, drawhp))

//Conditions

    pattern     = patterndetected and not patterndetected[1]
    pattern

pivotsdir_f(dynlength, pivots, pivotscount, pivotsdir)

patterndetected = patterndetection_f(pivots, pivotscount, pivotsdir, patternlines, patnewlabel, patterntype, patternlabels, leg, ratiolines, ratios, targets, targetslabels, dynlength)

//◀─── Alerts ───►

if patterndetected
    alert('New Harmonic Pattern Detected! • ' + str.tostring(close), alert.freq_once_per_bar)