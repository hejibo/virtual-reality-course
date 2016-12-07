import viz
viz.go()

model = viz.add('art/poly difference.ive' )

import vizcam
nav = vizcam.PivotNavigate()
nav.setCenter(0,1.2,0)
nav.setDistance(3.5)
import vizinfo
vizinfo.add('Hit F3 to see textures, then polygons, then vertices')


#viz.MainView.getHeadLight().disable()
#l1 = viz.addLight()
#l1.position( 0,1,-1,0 )



