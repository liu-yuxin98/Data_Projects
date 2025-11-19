package org.example;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import java.time.Duration;

import org.apache.flink.streaming.api.windowing.assigners.GlobalWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.triggers.CountTrigger;
import org.apache.flink.util.Collector;

public class WindowWordCount {

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        //test
//        DataStream<Tuple2<String, Integer>> dataStream = env
//                .fromElements(
//                        "hello world",
//                        "flink streaming",
//                        "hello flink"
//                )
//                .flatMap(new Splitter())
//                .keyBy(value -> value.f0)
//                .window(GlobalWindows.create())
//                .trigger(CountTrigger.of(1))
//                .sum(1);


        DataStream<Tuple2<String, Integer>> dataStream = env
                .socketTextStream("localhost", 9999)
                .flatMap(new Splitter())
                .keyBy(value -> value.f0)
                .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
                .sum(1);

        dataStream.print();

        env.execute("Window WordCount");

    }

    public static class Splitter implements FlatMapFunction<String, Tuple2<String, Integer>> {
        @Override
        public void flatMap(String sentence, Collector<Tuple2<String, Integer>> out) throws Exception {
            System.out.println("Received sentence: " + sentence);
            for (String word: sentence.split(" ")) {
                System.out.println("Emitting: " + word);
                out.collect(new Tuple2<String, Integer>(word, 1));
            }
        }
    }

}
