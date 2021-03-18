#!/usr/bin/env python
import os
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry, OccupancyGrid
from gazebo_msgs.msg import LinkStates
import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, XSD, OWL,URIRef

import csv

CORA = Namespace("http://www.semanticweb.org/ontologies/2013/7/CORA.owl#")
FR = Namespace("http://github.com/Alex23013/slam-up/FortesRey.owl#")
ISRO = Namespace("http://github.com/Alex23013/slam-up/ISRO.owl#")
OS = Namespace("http://github.com/Alex23013/slam-up/OntoSLAM.owl#")
KN= Namespace("http://knowrob.org/kb/knowrob.owl")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

class Server:
  def __init__(self):
    self.m_pose = None
    self.m_map = None
    self.m_link = None

  def pose_callback(self, msg):
    self.m_pose = msg
    self.compute_pose()

  def link_callback(self, msg):
    self.m_link = msg

  def map_callback(self, msg):
    self.m_map = msg

  def compute_pose(self):
    if self.m_pose is not None :       
      robot_position = self.m_pose.pose.pose.position
      robot_orientation =self.m_pose.pose.pose.orientation
      robot_uncertainty =self.m_pose.pose.covariance

      #To determine the robot state
      robot_linear_velocity = self.m_pose.twist.twist.linear
      robot_angular_velocity = self.m_pose.twist.twist.angular
      seq = self.m_pose.header.seq
      stamp = self.m_pose.header.stamp
      print(stamp.nsecs)
      if stamp.nsecs % 100000 == 0 : ## 1 lectura por segundo aprox #10000000
        g = rdflib.Graph() 
        print "listen odom"
        
        t_bot=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot')
        t_bot_pose=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot_pose')#rule
        struct_model=URIRef('http://github.com/Alex23013/slam-up/individual/struct_model')
        base_link=URIRef('http://github.com/Alex23013/slam-up/individual/base_link')

        base_visual=URIRef('http://github.com/Alex23013/slam-up/individual/base_visual')
        base_link_height=URIRef('http://github.com/Alex23013/slam-up/individual/base_link_height')
        base_link_width=URIRef('http://github.com/Alex23013/slam-up/individual/base_link_width')
        base_link_depth=URIRef('http://github.com/Alex23013/slam-up/individual/base_link_depth')

        base_footprint=URIRef('http://github.com/Alex23013/slam-up/individual/base_footprint')
        base_joint=URIRef('http://github.com/Alex23013/slam-up/individual/base_joint')
        
        box_shape=URIRef('http://github.com/Alex23013/slam-up/individual/box_shape')
        cylinder_shape=URIRef('http://github.com/Alex23013/slam-up/individual/cylinder_shape')
        color_black=URIRef('http://github.com/Alex23013/slam-up/individual/color_black')
        color_gray=URIRef('http://github.com/Alex23013/slam-up/individual/color_gray')
        
        base_shape_prob=URIRef('http://github.com/Alex23013/slam-up/individual/base_shape_prob')
        base_state=URIRef('http://github.com/Alex23013/slam-up/individual/base_state')
        mobile_true=URIRef('http://github.com/Alex23013/slam-up/individual/mobile_true')
        reconfigurable_true=URIRef('http://github.com/Alex23013/slam-up/individual/reconfigurable_true')

        base_axis=URIRef('http://github.com/Alex23013/slam-up/individual/base_axis')
        base_z_axis=URIRef('http://github.com/Alex23013/slam-up/individual/base_z_axis')
        vector_base=URIRef('http://knowrob.org/kb/knowrob.owl/individual/vector_base')
        vector_z_base=URIRef('http://knowrob.org/kb/knowrob.owl/individual/vector_z_base')

        wheel_left_link=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_left_link')        
        wheel_left_joint=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_left_joint')
        wheel_left_visual=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_left_visual')
        wheel_right_link=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_right_link')
        wheel_right_joint=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_right_joint')
        wheel_right_visual=URIRef('http://github.com/Alex23013/slam-up/individual/wheel_right_visual')

        base_scan_link=URIRef('http://github.com/Alex23013/slam-up/individual/base_scan_link')        
        base_scan_joint=URIRef('http://github.com/Alex23013/slam-up/individual/base_scan_joint')
        base_scan_visual=URIRef('http://github.com/Alex23013/slam-up/individual/base_scan_visual')

        pos_base_link=URIRef('http://github.com/Alex23013/slam-up/individual/pos_base_link')
        t_bot_trans=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot_trans')
        t_bot_orient=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot_orient')
        t_bot_stamp=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot_stamp')
        t_bot_prob=URIRef('http://github.com/Alex23013/slam-up/individual/t_bot_prob')
        pos_cov_mat=URIRef('http://github.com/Alex23013/slam-up/individual/pos_cov_mat')


        g.add((color_black, OS.hasRGBValue, Literal("(0,0,0)", datatype=XSD.string)))
        g.add((color_gray, OS.hasRGBValue, Literal("(166, 166, 166)", datatype=XSD.string)))
        g.add((box_shape, RDF.type, OS.Box))
        g.add((cylinder_shape, RDF.type, OS.Box))

        g.add((t_bot, RDF.type, CORA.Robot))
        g.add((mobile_true, RDF.type, OS.Mobile))
        g.add((mobile_true, OS.mobileValue, Literal(True, datatype=XSD.boolean)))
        g.add((t_bot, OS.isMobile, mobile_true ))
        
        g.add((reconfigurable_true, RDF.type, OS.Reconfigurable))
        g.add((reconfigurable_true, OS.reconfigurableValue, Literal(True, datatype=XSD.boolean)))
        g.add((t_bot, OS.isReconfigurable, reconfigurable_true))

        g.add((struct_model, RDF.type, OS.StructuralModel))
        g.add( (t_bot, OS.hasModel , struct_model ) )
        g.add((t_bot_pose, RDF.type, OS.Pose))
        g.add( (t_bot, OS.hasPose , t_bot_pose) )

        #cat1
        g.add((base_link, RDF.type, OS.BasePart))
        g.add((struct_model, OS.hasPart , base_link ))
        g.add((base_state, RDF.type, OS.State))
        if(robot_linear_velocity.x == 0.0 and robot_linear_velocity.y == 0.0 and robot_angular_velocity.x == 0.0 and robot_angular_velocity.y == 0.0):
          g.add((base_state, OS.hasStateValue, Literal("NotMoved", datatype=XSD.string)))
        else:  
          g.add((base_state, OS.hasStateValue, Literal("Moved", datatype=XSD.string)))

        
        g.add((pos_base_link, RDF.type, OS.Position))
        g.add((base_link, OS.hasPosition , pos_base_link) )
        g.add((pos_base_link, OS.hasTranslation, t_bot_trans))
        g.add((pos_base_link, OS.hasOrientation, t_bot_orient))
        g.add((struct_model, OS.hasPosition , pos_base_link) ) # inference_rule
        g.add((t_bot_pose, OS.isComposedBy,struct_model))
        g.add( (t_bot_trans, RDF.type, FR.cartesianPositionPoint))
        g.add( (t_bot_trans, CORA.cartesianX, Literal(robot_position.x, datatype=OWL.real) ) )
        g.add( (t_bot_trans, CORA.cartesianY, Literal(robot_position.y, datatype=OWL.real) ) )
        g.add( (t_bot_trans, CORA.cartesianZ, Literal(robot_position.z, datatype=OWL.real) ) )

        g.add((t_bot_orient, RDF.type, CORA.OrientationValue))
        g.add( (t_bot_orient, OS.componentY, Literal(robot_orientation.y, datatype=OWL.real) ) )
        g.add( (t_bot_orient, OS.componentX, Literal(robot_orientation.x, datatype=OWL.real) ) )
        g.add( (t_bot_orient, OS.componentZ, Literal(robot_orientation.z, datatype=OWL.real) ) )
        g.add( (t_bot_orient, OS.componentW, Literal(robot_orientation.w, datatype=OWL.real) ) )

        g.add((t_bot_stamp, RDF.type, ISRO.TimePoint))
        g.add( (pos_base_link, OS.posAtTime , t_bot_stamp ) )
        g.add( (t_bot_stamp, OS.hasStamp, Literal(stamp, datatype=OWL.real)) )
        g.add((t_bot_prob, RDF.type, OS.Probability))
        g.add((pos_base_link, OS.hasProbability, t_bot_prob))

        g.add((pos_cov_mat, RDF.type, OS.CovarianceMatrix))
        g.add((t_bot_prob, OS.hasMatrixValue, pos_cov_mat))
		
        for i, val in enumerate(robot_uncertainty): 
          if val != 0.0:
            #print "(",(i/6), "-",(i%6), ",",val,")" #row,col,val      
            covariance_val= BNode()
            g.add( (covariance_val, RDF.type , OS.MatrixElement ) )
            g.add( (covariance_val, OS.belongs_to , pos_cov_mat ) )
            g.add( (covariance_val, OS.componentRow, Literal(i/6, datatype=XSD.NonNegativeInteger) ) )
            g.add( (covariance_val, OS.componentCol, Literal(i%6, datatype=XSD.NonNegativeInteger) ) )
            g.add( (covariance_val, OS.componentValue, Literal(val, datatype=OWL.real) ) )
        self.compute_map(g, stamp)
        #self.compute_link(g, stamp, struct_model)
        namefile = 'out/out_turtle_map_'+str(seq)+'.owl'
        print(namefile)
        s = g.serialize(destination=namefile,format='turtle')
        
        ##Cloud        
        #myCmd = 'gsutil -m cp ./'+namefile+'  gs://slam-up-bucket1'
        #os.system(myCmd)
        
        
    else:
      rospy.loginfo("i can't hear pose")
      
  def compute_link(self, g, stamp, struct_model):
    links = self.m_link.name
    print("links encontrados")
    print(links)
    pos = self.m_link.pose
    cont = 0
    for i in pos:
      link_name = links[cont][links[cont].find("::")+2:]
      
      link=URIRef('http://github.com/Alex23013/slam-up/individual/'+link_name)        
      pos=URIRef('http://github.com/Alex23013/slam-up/individual/pos_'+link_name)
      trans=URIRef('http://github.com/Alex23013/slam-up/individual/trans_'+link_name)
      orient=URIRef('http://github.com/Alex23013/slam-up/individual/orient_'+link_name)
      if links[cont].find("turtlebot3") != -1 and links[cont] != "turtlebot3_burger::base_footprint":
        print ("pos de "+link_name)
        g.add((link, RDF.type, OS.AtomicPart))
        g.add((pos, RDF.type, OS.Position))
        g.add((link, OS.hasPosition , pos ) )
        g.add((struct_model, OS.hasPart ,link ))
        g.add( (trans, RDF.type, FR.cartesianPositionPoint))
        g.add( (trans, CORA.cartesianX, Literal(i.position.x, datatype=OWL.real) ) )
        g.add( (trans, CORA.cartesianY, Literal(i.position.y, datatype=OWL.real) ) )
        g.add( (trans, CORA.cartesianZ, Literal(i.position.z, datatype=OWL.real) ) )
        g.add((orient, RDF.type, CORA.OrientationValue))
        g.add((orient, OS.componentY, Literal(i.orientation.y, datatype=OWL.real) ) )
        g.add((orient, OS.componentX, Literal(i.orientation.x, datatype=OWL.real) ) )
        g.add((orient, OS.componentZ, Literal(i.orientation.z, datatype=OWL.real) ) )
        g.add((orient, OS.componentW, Literal(i.orientation.w, datatype=OWL.real) ) )
        g.add((pos, OS.hasTranslation, trans))
        g.add((pos, OS.hasOrientation, orient))

      cont=cont+1

  def compute_map(self, g, stamp):
    if self.m_map is not None :
      resolution = self.m_map.info.resolution
      width = self.m_map.info.width
      height = self.m_map.info.height
      map = self.m_map.data
      print "map readed of",len(map),"cells"

      env_link=URIRef('http://github.com/Alex23013/slam-up/individual/env_link')
      env_visual=URIRef('http://github.com/Alex23013/slam-up/individual/env_visual')
      env_shape=URIRef('http://github.com/Alex23013/slam-up/individual/env_shape')
      env_height=URIRef('http://github.com/Alex23013/slam-up/individual/env_height')
      env_width=URIRef('http://github.com/Alex23013/slam-up/individual/env_width')
      env_stamp=URIRef('http://github.com/Alex23013/slam-up/individual/env_stamp')

      g.add((env_link, RDF.type, CORA.Environment))
      g.add((env_visual, RDF.type, OS.Visual))
      g.add((env_link, OS.hasVisual, env_visual))
      g.add((env_shape, RDF.type, OS.OccupancyGrid))
      g.add((env_visual, OS.hasShape, env_shape))
      g.add((env_visual, OS.hasDimension, env_height))
      g.add((env_visual, OS.hasDimension, env_width))
      g.add((env_height, RDF.type, OS.Height))
      g.add((env_width, RDF.type, OS.Width))

      g.add( (env_width,OS.hasValue, Literal(width, datatype=XSD.NonNegativeInteger) ) ) 
      g.add( (env_height,OS.hasValue, Literal(height, datatype=XSD.NonNegativeInteger) ) ) 
      g.add( (env_shape,OS.has_resolution, Literal(resolution, datatype=XSD.NonNegativeInteger) ) ) 
      g.add( (env_stamp, RDF.type, ISRO.TimePoint))
      g.add( (env_stamp, OS.hasStamp, Literal(stamp, datatype=OWL.real)) )
      for i, val in enumerate(map): 
       if val != -1:
        row=str(i/height)
        col = str(i%height)    
        obj=URIRef('http://github.com/Alex23013/slam-up/individual/obj/'+row+'_'+col)
        obj_joint=URIRef('http://github.com/Alex23013/slam-up/individual/obj_joint/'+row+'_'+col)
        obj_pos=URIRef('http://github.com/Alex23013/slam-up/individual/obj_pos/'+row+'_'+col)
        obj_trans=URIRef('http://github.com/Alex23013/slam-up/individual/obj_trans/'+row+'_'+col)
        obj_prob=URIRef('http://github.com/Alex23013/slam-up/individual/obj_prob/'+row+'_'+col)

        g.add((obj, RDF.type, OS.AtomicPart))
        g.add((obj_joint, RDF.type, OS.FixedJoint))
        g.add((obj_joint, OS.hasParent,env_link ))
        g.add((obj_joint, OS.hasChild,obj ))
        g.add((obj_pos, RDF.type, OS.Position))
        g.add((obj, OS.hasPosition,obj_pos ))
        g.add((obj_pos, OS.hasTranslation, obj_trans))
        g.add((obj_trans, RDF.type, FR.cartesianPositionPoint))
        g.add((obj_trans, CORA.cartesianX, Literal(i/height, datatype=OWL.real) ) )
        g.add((obj_trans, CORA.cartesianY, Literal(i%height, datatype=OWL.real) ) )
        g.add((obj_prob, RDF.type, OS.Probability))
        g.add((obj_pos, OS.hasProbability, obj_prob))
        g.add((obj_prob, OS.hasNumberValue, Literal(val, datatype=OWL.real)))
        
        g.add( (obj_pos, OS.posAtTime , env_stamp ) )
        

      self.m_map = None  
    else:
      rospy.loginfo('i cant hear map')

def listener():

    rospy.init_node('listener', anonymous=True)
    server = Server()
    rospy.Subscriber("odom", Odometry , server.pose_callback)
    rospy.Subscriber("map", OccupancyGrid, server.map_callback)
    rospy.Subscriber("gazebo/link_states", LinkStates , server.link_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
